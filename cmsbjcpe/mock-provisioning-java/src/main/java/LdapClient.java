import java.io.IOException;
import java.security.GeneralSecurityException;
import java.security.KeyStoreException;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.net.ssl.SSLContext;

import com.unboundid.ldap.sdk.Entry;
import com.unboundid.ldap.sdk.ExtendedRequest;
import com.unboundid.ldap.sdk.ExtendedResult;
import com.unboundid.ldap.sdk.FailoverServerSet;
import com.unboundid.ldap.sdk.LDAPConnection;
import com.unboundid.ldap.sdk.LDAPConnectionOptions;
import com.unboundid.ldap.sdk.LDAPConnectionPool;
import com.unboundid.ldap.sdk.LDAPConnectionPoolHealthCheck;
import com.unboundid.ldap.sdk.LDAPException;
import com.unboundid.ldap.sdk.ResultCode;
import com.unboundid.ldap.sdk.SimpleBindRequest;
import com.unboundid.ldap.sdk.StartTLSPostConnectProcessor;
import com.unboundid.ldap.sdk.extensions.StartTLSExtendedRequest;
import com.unboundid.ldif.LDIFException;
import com.unboundid.util.Debug;
import com.unboundid.util.LDAPTestUtils;
import com.unboundid.util.ssl.KeyStoreKeyManager;
import com.unboundid.util.ssl.SSLUtil;
import com.unboundid.util.ssl.TrustStoreTrustManager;

public class LdapClient {

	/**
	 * @param args
	 */
	public static void main(String[] args) {

		LdapClient client = new LdapClient();
		client.tlsBind();

	}

	public void tlsBind() {

		try {
			Debug.setEnabled(true);
			Logger logger = Debug.getLogger();

			FileHandler fileHandler = new FileHandler("/tmp/cert.log");
			fileHandler.setLevel(Level.FINE);
			logger.addHandler(fileHandler);
			Debug.setIncludeStackTrace(true);
			com.unboundid.util.Debug.getLogger().setLevel(java.util.logging.Level.FINEST);
			SSLUtil sslUtil = new SSLUtil(new TrustStoreTrustManager("c:/tmp/truststore.jks"));
			SSLContext sslContext = sslUtil.createSSLContext();

			System.out.println("SSLContext::" + sslContext);

			LDAPConnection connection = new LDAPConnection("lijia.com", 1389);

			StartTLSExtendedRequest startTLSRequest = new StartTLSExtendedRequest(sslContext);
			ExtendedResult startTLSResult = connection.processExtendedOperation(startTLSRequest);
			
			String[] ldifAttrs = {
		            "dn: imsi=12345,dc=ihssdit",
		            "changetype:add",
		            "objectClass: top",
		            "objectClass: AccessData",
		            "imsi:12345"
		            };
			connection.add(ldifAttrs);
			System.out.println("Output ::" + connection.getConnectedAddress());
			connection.close();
		} catch (KeyStoreException e) {
			e.printStackTrace();
		} catch (LDAPException e) {
			System.out.println("LDAP Exception:" + e.getMessage());

			e.printStackTrace();
		} catch (GeneralSecurityException e) {
			e.printStackTrace();
		} catch (SecurityException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (LDIFException e) {
			e.printStackTrace();
		}finally {
		}
	}

}
