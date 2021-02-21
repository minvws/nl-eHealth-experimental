package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/asn1"
	"encoding/pem"
	"github.com/go-errors/errors"
	"github.com/privacybydesign/gabi"
	"github.com/privacybydesign/gabi/big"
	"golang.org/x/crypto/sha3"
	gobig "math/big"
	"os"
	"strconv"
	"time"
	"fmt"
)

// NOTE: This example is still experimental in this implementation and use-case, and subject to peer-review
func main() {
	fmt.Println("Generating new safeprime keypair... (this can take a minute)")

	// Use 1024 bits keys for demo purposes (faster key generation)
	params := gabi.DefaultSystemParameters[1024]

	// Generate deterministic Idemix keypair
	privk, pubk, err := generateDeterministicKeyPair(params)
	if err != nil {
		panic("Could not generate keypair")
	}

	// Create RSA keypair from Idemix keys
	rsaPrivk, rsaPubk, err := rsaKeypairFromGabi(privk, pubk)
	if err != nil {
		panic("Could not create RSA keypair")
	}

	err = rsaPrivk.Validate()
	if err != nil {
		panic("Invalid private key")
	}

	// Create self-signed certificate
	template := x509.Certificate{
		SerialNumber: gobig.NewInt(1),
		Subject: pkix.Name{
			Organization: []string{"Acme Co"},
		},
		NotBefore:             time.Now(),
		NotAfter:              time.Now(),
		KeyUsage:              x509.KeyUsageDigitalSignature,
		BasicConstraintsValid: true,
	}

	derBytes, err := x509.CreateCertificate(rand.Reader, &template, &template, rsaPubk, rsaPrivk)

	// Write self-signed certificate (including pubkey)
	certFilename := "cert.pem"
	certOut, _ := os.Create(certFilename)
	pem.Encode(certOut, &pem.Block{Type: "CERTIFICATE", Bytes: derBytes})

	fmt.Printf("\nWritten self-signed classic RSA certificate with Idemix modulus: %s\n", certFilename)

	// Write Idemix private key
	privkeyFilename := "privkey.pem"
	privKeyOut, _ := os.Create(privkeyFilename)
	privk.WriteTo(privKeyOut)

	fmt.Printf("Written Idemix private key: %s\n", privkeyFilename)
}

func rsaKeypairFromGabi(privk *gabi.PrivateKey, pubk *gabi.PublicKey) (*rsa.PrivateKey, *rsa.PublicKey, error) {
	bigOne := gobig.NewInt(1)

	primes := []*gobig.Int{privk.P.Go(), privk.Q.Go()}

	n := new(gobig.Int).Set(bigOne)
	totient := new(gobig.Int).Set(bigOne)
	pminus1 := new(gobig.Int)
	for _, prime := range primes {
		n.Mul(n, prime)
		pminus1.Sub(prime, bigOne)
		totient.Mul(totient, pminus1)
	}

	if n.BitLen() != int(pubk.Params.Ln) {
		return nil, nil, errors.Errorf("Could not create public key (unlikely error)")
	}

	rsaPrivk := new(rsa.PrivateKey)
	rsaPrivk.Primes = primes
	rsaPrivk.N = pubk.N.Go()
	rsaPrivk.E = 65537

	rsaPrivk.D = new(gobig.Int)
	e := gobig.NewInt(int64(rsaPrivk.E))
	ok := rsaPrivk.D.ModInverse(e, totient)
	if ok == nil {
		return nil, nil, errors.Errorf("Could not create public key (invalid parameter D)")
	}

	rsaPrivk.Precompute()
	return rsaPrivk, rsaPrivk.Public().(*rsa.PublicKey), nil
}

func generateDeterministicKeyPair(params *gabi.SystemParameters) (*gabi.PrivateKey, *gabi.PublicKey, error) {
	privk, originalPubk, err := gabi.GenerateKeyPair(params, 0, 0, time.Now())
	if err != nil {
		return nil, nil, err
	}

	privk.ECDSA = ""
	pubk := deterministicPubkeyFromN(params, originalPubk.N, 12)

	return privk, pubk, nil
}

// TODO: This function is still experimental in this implementation and use-case, and subject to peer-review
func deterministicPubkeyFromN(params *gabi.SystemParameters, N *big.Int, numAttributes int) *gabi.PublicKey {
	s := hashNForPrefix(params, "S", N)
	z := hashNForPrefix(params, "Z", N)

	rs := make([]*big.Int, 0, numAttributes)
	for i := 0; i < numAttributes; i++ {
		r := hashNForPrefix(params, "R"+strconv.Itoa(i), N)
		rs = append(rs, r)
	}

	return gabi.NewPublicKey(N, z, s, nil, nil, rs, "", 0, time.Now())
}

func hashNForPrefix(params *gabi.SystemParameters, prefix string, N *big.Int) *big.Int {
	if len(prefix) == 0 {
		panic("Invalid empty prefix")
	}

	hashBts, _ := asn1.Marshal(struct {
		Prefix []byte
		N      []byte
	}{Prefix: []byte(prefix), N: N.Bytes()})

	return hash(params, N, hashBts)
}

// TODO: This function is still experimental in this implementation and use-case
// Hash returns the output of a cryptographic hash function applied to the specified bytes.
//
// The hash is constructed as SHAKE256(bts)^2 mod n.
func hash(param *gabi.SystemParameters, N *big.Int, bts []byte) *big.Int {
	output := make([]byte, param.Ln/8) // pubk.Params.Ln is in bits, not bytes
	x := new(big.Int)
	max := new(big.Int).Rsh(N, 1)

	// Compute H(i || bts) with increasing i until the output is smaller than (n-1)/2
	for i := 0; i == 0 || x.Cmp(max) >= 0; i++ {
		asn, _ := asn1.Marshal(struct { // error never errors
			A int
			B []byte
		}{A: i, B: bts})
		sha3.ShakeSum256(output, asn)
		x.SetBytes(output).Rsh(x, 1) // We want not Ln but Ln-1 bits
	}

	return x.Mul(x, x).Mod(x, N) // embed in QR_n by squaring mod n
}
