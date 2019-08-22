package hello;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.SynchronousQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.amqp.AmqpException;
import org.springframework.amqp.core.MessageProperties;
import org.springframework.amqp.rabbit.core.ChannelCallback;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.AMQP.BasicProperties;
import com.rabbitmq.client.Channel;

@Component
public class Runner implements CommandLineRunner {
	protected final Log logger = LogFactory.getLog(getClass());
	private final RabbitTemplate rabbitTemplate;
	private final Receiver receiver;

	public Runner(Receiver receiver, RabbitTemplate rabbitTemplate) {
		this.receiver = receiver;
		this.rabbitTemplate = rabbitTemplate;
	}

	@Override
	public void run(String... args) throws Exception {
		final ThreadPoolExecutor executor = new ThreadPoolExecutor(0, Integer.MAX_VALUE,
                60L, TimeUnit.SECONDS,
                new SynchronousQueue<Runnable>());
		if(Application.tag.indexOf("s")<0) {
			logger.info("sender disabled..");
			
		}else {
			logger.info("sender enabled..");
			for (int i = 0; i < Application.count; i++) {
				final int ii = i;

				
				logger.info("Before sending message...." + ii);
				try {
					executor.execute(new Runnable() {

						@Override
						public void run() {
							try {
								rabbitTemplate.execute(new ChannelCallback<String>() {
									@Override
									public String doInRabbit(Channel channel) throws Exception {
										AMQP.BasicProperties.Builder props = new AMQP.BasicProperties.Builder();
										HashMap<String, Object> headers = new HashMap<String, Object>();
										headers.put("x-delay", 5000);
										props.headers(headers);
										channel.basicPublish(Application.topicExchangeName, "foo.bar.bazqwe", props.build(),
												("Hello from RabbitMQ!" + ii).getBytes());
										logger.info("After sending message...." + ii);
										return "";
									}
								});
							} catch (Exception e) {
								// retry this work when it fails.
								executor.execute(this);
							}
						}

					});

				} catch (AmqpException e) {
					logger.info(e.getMessage(), e);
				}
			}

		}
		
		receiver.getLatch().await(1000000, TimeUnit.MILLISECONDS);
		logger.info(receiver.report());
		executor.shutdown();
	}

//	@Override
//	public void run(String... args) throws Exception {
//		for(int i= 0;i<10000;i++) {
//			final int ii = i;
//			logger.info("Before sending message...."+ii);
//		try {
//	        this.rabbitTemplate.execute(new ChannelCallback<String>() {
//	            @Override
//	            public String doInRabbit(Channel channel) throws Exception {
//	            	AMQP.BasicProperties.Builder props = new AMQP.BasicProperties.Builder();
//	            	HashMap<String, Object> headers = new HashMap<String, Object>();
//	            	headers.put("x-delay", 5000);
//	            	props.headers(headers);
//	            	channel.basicPublish(Application.topicExchangeName, "foo.bar.bazqwe", props.build(), ("Hello from RabbitMQ!"+ii).getBytes());
//	            	logger.info("After sending message...."+ii);
//	            	return "";
//	            }
//	        });
//	    } catch ( AmqpException e ) {
//	        logger.info(e.getMessage(),e);
//	    }
//		}
//
//		receiver.getLatch().await(1000000, TimeUnit.MILLISECONDS);
//	}
//	@Override
//	public void run(String... args) throws Exception {
//		for(int i= 0;i<100000;i++) {
//			logger.info("Sending message...."+i);
//			rabbitTemplate.convertAndSend(Application.topicExchangeName, "foo.bar.bazqwe", "Hello from RabbitMQ!"+i, m -> {
//				m.getMessageProperties().setDelay(10000);
//				logger.info("Sending message.........");
//				return m;
//			});
//		}
//		
//		receiver.getLatch().await(1000000, TimeUnit.MILLISECONDS);
//	}

}
