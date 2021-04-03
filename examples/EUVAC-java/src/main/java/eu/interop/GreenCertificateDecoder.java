package eu.interop;

import static org.apache.commons.compress.utils.IOUtils.toByteArray;

import COSE.CoseException;
import COSE.Message;
import COSE.MessageTag;
import COSE.OneKey;
import COSE.Sign1Message;
import com.upokecenter.cbor.CBORObject;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import org.apache.commons.compress.compressors.CompressorException;
import org.apache.commons.compress.compressors.CompressorInputStream;
import org.apache.commons.compress.compressors.CompressorStreamFactory;

public class GreenCertificateDecoder {

    private final OneKey publicKey;

    public GreenCertificateDecoder(OneKey publicKey) {
        this.publicKey = publicKey;
    }

    /**
     * Decodes base45 encoded string -> Deflate -> COSE -> CBOR -> arbitrary Json String
     *
     * @param base45String
     * @return
     * @throws CompressorException
     * @throws IOException
     * @throws CoseException
     */
    public String decode(String base45String) throws CompressorException, IOException, CoseException {
        byte[] decodedBytes = Base45.decode(base45String);

        byte[] coseBytes = getCoseBytes(decodedBytes);

        byte[] cborBytes = getCborBytes(coseBytes);

        return getJsonString(cborBytes);
    }

    private String getJsonString(byte[] cborBytes) throws IOException {
        CBORObject cborObject = CBORObject.DecodeFromBytes(cborBytes);
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        cborObject.WriteJSONTo(byteArrayOutputStream);

        return byteArrayOutputStream.toString("UTF-8");
    }

    private byte[] getCborBytes(byte[] coseBytes) throws CoseException {
        Sign1Message msg = (Sign1Message) Message.DecodeFromBytes(coseBytes, MessageTag.Sign1);
        if (!msg.validate(publicKey))
            throw new RuntimeException("Could not verify COSE signature");

        return msg.GetContent();
    }

    private byte[] getCoseBytes(byte[] decodedBytes) throws CompressorException, IOException {

        CompressorInputStream compressedStream = new CompressorStreamFactory()
                .createCompressorInputStream(CompressorStreamFactory.DEFLATE, new ByteArrayInputStream(decodedBytes));

        return toByteArray(compressedStream);
    }
}
