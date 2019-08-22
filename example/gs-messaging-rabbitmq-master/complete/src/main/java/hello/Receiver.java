package hello;

import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.stereotype.Component;

@Component
public class Receiver {

	protected final Log logger = LogFactory.getLog(getClass());
    private CountDownLatch latch;
    private AtomicInteger successCount = new AtomicInteger(0);
    public Receiver() {
    	latch = new CountDownLatch(Application.count);
    }
    
    public void receiveMessage(byte[] message) {
    	logger.info("Received <" + new String(message) + ">");
        latch.countDown();
        successCount.addAndGet(1);
    }

    public CountDownLatch getLatch() {
        return latch;
    }
    public String report() {
    	return "success receive message:"+successCount.get();
    }
}
