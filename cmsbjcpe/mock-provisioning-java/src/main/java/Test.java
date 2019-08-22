import javax.net.ssl.SSLContext;

import com.unboundid.ldap.sdk.ExtendedResult;
import com.unboundid.ldap.sdk.LDAPConnection;
import com.unboundid.ldap.sdk.LDAPResult;
import com.unboundid.ldap.sdk.extensions.StartTLSExtendedRequest;
import com.unboundid.util.ssl.SSLUtil;
import com.unboundid.util.ssl.TrustStoreTrustManager;

public class Test extends Thread{

	private String id;
	public static void main(String[] args) {
		int runner = 2;
		for(int i = 1;i<=runner;i++) {
			new Test(i+"").start();
		}
		
	}

	public Test(String id) {
		super();
		this.id = id;
	}

	public void run() {
		for(int i = 0;i< 1;i++) {
			runTest(id+i);
		}
	}
	void runTest(String imsi) {
		try {
			
//			Debug.setEnabled(true);
//			Logger logger = Debug.getLogger();
//
//			FileHandler fileHandler = new FileHandler("/tmp/cert.log");
//			fileHandler.setLevel(Level.FINE);
//			logger.addHandler(fileHandler);
//			Debug.setIncludeStackTrace(true);
//			com.unboundid.util.Debug.getLogger().setLevel(java.util.logging.Level.FINEST);
			SSLUtil sslUtil = new SSLUtil(new TrustStoreTrustManager("c:/tmp/truststore.jks"));
//			sslUtil.setDefaultSSLProtocol(SSLUtil.SSL_PROTOCOL_TLS_1_3);
			SSLContext sslContext = sslUtil.createSSLContext();

			LDAPConnection connection = new LDAPConnection("lijiatest", 1389);

			StartTLSExtendedRequest startTLSRequest = new StartTLSExtendedRequest(sslContext);
			ExtendedResult startTLSResult = connection.processExtendedOperation(startTLSRequest);
			
//			LDAPTestUtils.assertResultCodeEquals(startTLSResult, ResultCode.SUCCESS);
			String[] ldifAttrs = {
		            "dn: imsi="+imsi+",dc=ihssdit",
		            "changetype:add",
		            "objectClass: top",
		            "objectClass: AccessData",
		            "imsi:"+imsi
		            };
			LDAPResult res = connection.add(ldifAttrs);
			System.out.println("Output ::" + ldifAttrs[0]+"  "+ res.getResultCode());
			connection.close();
		} catch (Exception e) {
			System.out.println("Output ::" + imsi);
			e.printStackTrace();
		}finally {
		}
	}
}
