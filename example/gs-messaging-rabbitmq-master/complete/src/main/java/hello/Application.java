package hello;

import java.util.HashMap;
import java.util.Map;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.listener.SimpleMessageListenerContainer;
import org.springframework.amqp.rabbit.listener.adapter.MessageListenerAdapter;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class Application {
	static int count = 10000;
	static String tag = "sr";
	protected final Log logger = LogFactory.getLog(getClass());
	static final String topicExchangeName = "spring-boot-exchange3";

	static final String queueName = "spring-boot3";

	@Bean
	Queue queue() {
		return new Queue(queueName, false);
	}

	@Bean
	TopicExchange exchange() {
		Map<String, Object> args = new HashMap<String, Object>();
		args.put("x-delayed-type", "direct");
		TopicExchange exchange = new TopicExchange(topicExchangeName, true, false, args);
		exchange.setDelayed(true);
		return exchange;
	}

	@Bean
	Binding binding(Queue queue, TopicExchange exchange) {
		return BindingBuilder.bind(queue).to(exchange).with("foo.bar.#");
	}

	@Bean
	SimpleMessageListenerContainer container(ConnectionFactory connectionFactory,
			MessageListenerAdapter listenerAdapter) {
		if(tag.indexOf("r")<0) {
			logger.info("reciver disabled..");
			return null;
		}
		logger.info("reciver enabled..");
		SimpleMessageListenerContainer container = new SimpleMessageListenerContainer();
		container.setConnectionFactory(connectionFactory);
		container.setQueueNames(queueName);
		container.setMessageListener(listenerAdapter);
		return container;
	}

	@Bean
	MessageListenerAdapter listenerAdapter(Receiver receiver) {
		return new MessageListenerAdapter(receiver, "receiveMessage");
	}

	public static void main(String[] args) throws InterruptedException {
		if(args!=null && args.length== 2) {
			count = Integer.parseInt(args[0]);
			tag = args[1].toLowerCase();
		}
		SpringApplication.run(Application.class, args).close();
	}

}
