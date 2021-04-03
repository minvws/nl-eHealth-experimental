package eu.interop;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import COSE.CoseException;
import COSE.KeyKeys;
import COSE.OneKey;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.upokecenter.cbor.CBORObject;
import java.io.IOException;
import org.apache.commons.compress.compressors.CompressorException;
import org.bouncycastle.asn1.nist.NISTNamedCurves;
import org.bouncycastle.asn1.x9.X9ECParameters;
import org.bouncycastle.crypto.AsymmetricCipherKeyPair;
import org.bouncycastle.crypto.generators.ECKeyPairGenerator;
import org.bouncycastle.crypto.params.ECDomainParameters;
import org.bouncycastle.crypto.params.ECKeyGenerationParameters;
import org.bouncycastle.crypto.params.ECPrivateKeyParameters;
import org.bouncycastle.crypto.params.ECPublicKeyParameters;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

public class CertificateTests {

  static OneKey cborPublicKey;
  static OneKey cborPrivateKey;

  String json =
      "\n" +
          "{\"legalName\":\"Gaby\",\"diseaseOrAgentTargeted\":\"Unknown\",\"startDateOfValidity\":\"2019-12-31\",\"personId\":\"ABC\",\"dateOfBirth\":\"2001-01-01\",\"gender\":\"F\",\"marketingAuthorizationHolder\":\"\",\"vaccineCode\":[{\"system\":\"urn:oid:1.2.36.1.2001.1005.17\"}],\"vaccineMedicinalProduct\":\"\",\"batchLotNumber\":\"\",\"dateOfVaccination\":\"\",\"administeringCentre\":\"\",\"healthProfessionalId\":\"\",\"countryOfVaccination\":\"\",\"numberInSeries\":\"\",\"nextVaccinationDate\":\"\",\"Total Matches\":70}";

  @BeforeAll
  static void beforeAll() throws Exception {
    AsymmetricCipherKeyPair asymmetricCipherKeyPair = buildRandomAsymmetricCipherKeyPair();

    ECPublicKeyParameters keyPublic = (ECPublicKeyParameters) asymmetricCipherKeyPair.getPublic();
    cborPublicKey = toCBORPublicKey(keyPublic);

    ECPrivateKeyParameters keyPrivate = (ECPrivateKeyParameters) asymmetricCipherKeyPair.getPrivate();
    cborPrivateKey = toCBORPrivateKey(keyPrivate);

  }

  static AsymmetricCipherKeyPair buildRandomAsymmetricCipherKeyPair() {
    X9ECParameters p = NISTNamedCurves.getByName("P-256");

    ECDomainParameters parameters = new ECDomainParameters(p.getCurve(), p.getG(), p.getN(),
        p.getH());
    ECKeyPairGenerator pGen = new ECKeyPairGenerator();
    ECKeyGenerationParameters genParam = new ECKeyGenerationParameters(parameters, null);
    pGen.init(genParam);
    return pGen.generateKeyPair();
  }

  static OneKey toCBORPrivateKey(ECPrivateKeyParameters keyPrivate) throws CoseException {
    CBORObject key;

    byte[] rgbD = keyPrivate.getD().toByteArray();

    key = CBORObject.NewMap();
    key.Add(KeyKeys.KeyType.AsCBOR(), KeyKeys.KeyType_EC2);
    key.Add(KeyKeys.EC2_Curve.AsCBOR(), KeyKeys.EC2_P256);
    key.Add(KeyKeys.EC2_D.AsCBOR(), rgbD);
    return new OneKey(key);
  }

  static OneKey toCBORPublicKey(ECPublicKeyParameters keyPublic) throws CoseException {
    byte[] rgbX = keyPublic.getQ().normalize().getXCoord().getEncoded();
    byte[] rgbY = keyPublic.getQ().normalize().getYCoord().getEncoded();

    CBORObject key = CBORObject.NewMap();
    key.Add(KeyKeys.KeyType.AsCBOR(), KeyKeys.KeyType_EC2);
    key.Add(KeyKeys.EC2_Curve.AsCBOR(), KeyKeys.EC2_P256);
    key.Add(KeyKeys.EC2_X.AsCBOR(), rgbX);
    key.Add(KeyKeys.EC2_Y.AsCBOR(), rgbY);
    return new OneKey(key);
  }


  @Test
  void coding() throws CompressorException, CoseException, IOException {

    String encoded = new GreenCertificateEncoder(cborPrivateKey).encode(json);
    String result = new GreenCertificateDecoder(cborPublicKey).decode(encoded);

    ObjectMapper mapper = new ObjectMapper();
    assertEquals(mapper.readTree(json), mapper.readTree(result));
  }

  @Test
  void codingWrongPublicKey() throws CompressorException, CoseException, IOException {

    AsymmetricCipherKeyPair p1 = buildRandomAsymmetricCipherKeyPair();
    OneKey anotherPublicKey = toCBORPublicKey((ECPublicKeyParameters) p1.getPublic());

    String encoded = new GreenCertificateEncoder(cborPrivateKey).encode(json);

    Exception exception = assertThrows(RuntimeException.class,
        () -> new GreenCertificateDecoder(anotherPublicKey).decode(encoded));
    assertEquals("Could not verify COSE signature", exception.getMessage());

  }
}
