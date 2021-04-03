package eu.interop;

import COSE.Attribute;
import COSE.AlgorithmID;
import COSE.CoseException;
import COSE.HeaderKeys;
import COSE.OneKey;
import COSE.Sign1Message;
import com.upokecenter.cbor.CBORObject;
import org.apache.commons.compress.compressors.CompressorException;
import org.apache.commons.compress.compressors.CompressorOutputStream;
import org.apache.commons.compress.compressors.CompressorStreamFactory;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;

public class GreenCertificateEncoder {

    private final OneKey privateKey;

    public GreenCertificateEncoder(OneKey privateKey) {
        this.privateKey = privateKey;
    }

    /**
     * Encodes arbitrary Json String to CBOR -> COSE -> Deflate -> BASE45
     *
     * @param json
     * @return
     * @throws CoseException
     * @throws CompressorException
     * @throws IOException
     */
    public String encode(String json) throws CoseException, CompressorException, IOException {
        System.out.println("Json size: " + json.length());

        byte[] cborBytes = getCborBytes(json);

        byte[] coseBytes = getCOSEBytes(cborBytes);

        byte[] deflateBytes = getDeflateBytes(coseBytes);

        String base45 = getBase45(deflateBytes);
        return base45;
    }

    private String getBase45(byte[] deflateBytes) throws UnsupportedEncodingException {
        String base45 = Base45.encode(deflateBytes);

        System.out.println("Base45 size: " + base45.getBytes("UTF-8").length);
        return base45;
    }

    private byte[] getDeflateBytes(byte[] messageBytes) throws CompressorException, IOException {
        ByteArrayOutputStream deflateOutputStream = new ByteArrayOutputStream();
        CompressorOutputStream deflateOut = new CompressorStreamFactory()
                .createCompressorOutputStream(CompressorStreamFactory.DEFLATE, deflateOutputStream);

        deflateOut.write(messageBytes);
        deflateOut.close();
        byte[] deflateBytes = deflateOutputStream.toByteArray();

        System.out.println("Deflate size: " + deflateBytes.length);
        return deflateBytes;
    }

    private byte[] getCOSEBytes(byte[] cborBytes) throws CoseException {
        Sign1Message msg = new Sign1Message();
        msg.addAttribute(HeaderKeys.Algorithm, AlgorithmID.ECDSA_256.AsCBOR(), Attribute.PROTECTED);
        msg.SetContent(cborBytes);
        msg.sign(privateKey);

        byte[] messageBytes = msg.EncodeToBytes();

        System.out.println("COSE size: " + messageBytes.length);
        return messageBytes;
    }

    private byte[] getCborBytes(String json) {
        CBORObject cborObject = CBORObject.FromJSONString(json);
        byte[] cborBytes = cborObject.EncodeToBytes();

        System.out.println("CBOR size: " + cborBytes.length);
        return cborBytes;
    }
}
