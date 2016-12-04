package com.saurav.Twitter.DataSerializer;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.LinkedBlockingQueue;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Properties;


import com.google.common.collect.Lists;
import com.twitter.hbc.ClientBuilder;
import com.twitter.hbc.core.Constants;
import com.twitter.hbc.core.endpoint.Location;
import com.twitter.hbc.core.endpoint.Location.Coordinate;
import com.twitter.hbc.core.endpoint.StatusesFilterEndpoint;
import com.twitter.hbc.core.endpoint.StatusesSampleEndpoint;
import com.twitter.hbc.core.processor.StringDelimitedProcessor;
import com.twitter.hbc.httpclient.BasicClient;
import com.twitter.hbc.httpclient.auth.Authentication;
import com.twitter.hbc.httpclient.auth.OAuth1;
import com.twitter.hbc.twitter4j.Twitter4jStatusClient;
import com.twitter.hbc.twitter4j.handler.StatusStreamHandler;
import com.twitter.hbc.twitter4j.message.DisconnectMessage;
import com.twitter.hbc.twitter4j.message.StallWarningMessage;

//import twitter4j.Logger;
import org.apache.log4j.Logger;
import twitter4j.StallWarning;
import twitter4j.Status;
import twitter4j.StatusDeletionNotice;
import twitter4j.StatusListener;
public class TwitterEnterpriseStream {

	final static Logger logger = Logger.getLogger(TwitterEnterpriseStream.class);
	final static Logger logger21 = Logger.getLogger("file");
	final static Logger logger3 = Logger.getLogger("admin"); 
	static Properties prop = new Properties();
	String myCategory;
	String mySubcategory;
	
// A bare bones listener
	  private StatusListener listener1 = new StatusListener() {
	    @Override
	    public void onStatus(Status status) {
	    	
	    	status.getCreatedAt();
	    	status.getFavoriteCount();
	    	status.getGeoLocation();
	    	status.getHashtagEntities();
	    	status.getLang();
	    	status.getURLEntities();
	    	status.getId();
	    	status.getUser().getLocation();
	    	status.getUser().getScreenName();
	    	status.getUser().getTimeZone();
	    	status.getUser().getId();
	    	
	    	//for (SymbolEntity i: status.getSymbolEntities())
	    	logger3.info(status.getId() +  status.getUser().getId() + status.getUser().getScreenName() +  status.getUser().getLocation() +  
	    	status.getText() + status.getCreatedAt() +   status.getGeoLocation());
	    	//System.out.println(status.getId() + ": " + status.getUser().getId() + ": " + status.getUser().getScreenName() + ": " + status.getUser().getLocation() + ": " + 
	    	  //  	status.getText() + ": " +status.getCreatedAt() +  ": " + status.getGeoLocation());
	    	
	    	System.out.println(status.getId() + status.getUser().getId() +  status.getUser().getScreenName() +  status.getUser().getLocation() + ": " + 
	    	    	status.getText() + status.getCreatedAt() +  status.getGeoLocation());
	    
	    	
	    			
	    	
	    }

	    @Override
	    public void onDeletionNotice(StatusDeletionNotice statusDeletionNotice) {}

	    @Override
	    public void onTrackLimitationNotice(int limit) {}

	    @Override
	    public void onScrubGeo(long user, long upToStatus) {}

	    @Override
	    public void onStallWarning(StallWarning warning) {
	    	
	    }

	    @Override
	    public void onException(Exception e) {
	    	System.out.println(e);
	    	
	    }
	  };

	  // A bare bones StatusStreamHandler, which extends listener and gives some extra functionality
	  private StatusListener listener2 = new StatusStreamHandler() {
	    @Override
	    public void onStatus(Status status) {
	    	
	    	status.getCreatedAt();
	    	status.getFavoriteCount();
	    	status.getGeoLocation();
	    	status.getHashtagEntities();
	    	status.getLang();
	    	status.getURLEntities();
	    	status.getId();
	    	status.getUser().getLocation();
	    	status.getUser().getScreenName();
	    	status.getUser().getTimeZone();
	    	status.getUser().getId();
	    	
	    	//for (SymbolEntity i: status.getSymbolEntities())
	    	//logger3.info(status.getId() + ": " + status.getUser().getId() + ": " + status.getUser().getScreenName() + ": " + status.getUser().getLocation() + ": " + 
	    	//status.getText() + ": " +status.getCreatedAt() +  ": " + status.getGeoLocation());
	    	
	    	logger3.info("\"" + status.getId() + "\"" +"," + "\""  + status.getUser().getId() + "\"" + "," + "\"" + status.getUser().getScreenName() + "\"" +"," 
	    	+ "\"" + status.getUser().getLocation() + "\"" +"," +  "\"" + createAudienceMsg(status.getText()) + "\"" +"," 
	    	+ "\"" + status.getCreatedAt() + "\"" +"," + "\"" + status.getGeoLocation() + "\"" +"," + "\"" + myCategory 
	    	+ "\"" +"," + "\"" + mySubcategory + "\"");
	    		    	
	    	
	    }

	    @Override
	    public void onDeletionNotice(StatusDeletionNotice statusDeletionNotice) {}

	    @Override
	    public void onTrackLimitationNotice(int limit) {}

	    @Override
	    public void onScrubGeo(long user, long upToStatus) {}

	    @Override
	    public void onStallWarning(StallWarning warning) {}

	    @Override
	    public void onException(Exception e) {}

	    @Override
	    public void onDisconnectMessage(DisconnectMessage message) {}

	    @Override
	    public void onStallWarningMessage(StallWarningMessage warning) {}

	    @Override
	    public void onUnknownMessageType(String s) {}
	  };
	  
	  private java.util.List<String> populateTwitterfields(String str, String def)
	  {
		  java.util.List<String> myList = new ArrayList();
		  String targetlist =  prop.getProperty(str, def);
		  myList = Arrays.asList(targetlist.split(" , "));
		  logger.info("Stub will fetch Tweets containing :" + str + " : "  +  myList.toString());
		  return myList;
		  
	  }
	  
	  private void parseconfiguration()
	  {
		  InputStream input = null;
		  try{ 
			  	input = new FileInputStream("src/main/resources/config.properties");
				prop.load(input);
				
				myCategory = prop.getProperty("iab-category","Unknown");
				mySubcategory = prop.getProperty("iab-sub-Category","Unknown");
				
				System.out.println(prop.getProperty("key-words","Travel"));
				System.out.println(prop.getProperty("language","en"));
				System.out.println(prop.getProperty("location", ""));
				;
			}catch (IOException ex) {
				ex.printStackTrace();
			} finally {
				if (input != null) {
					try {
						input.close();
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
			}
	  }
	  public String createAudienceMsg(String str)
	  {
		  
//		  String replaced = str.replaceAll("\\", "\\\\")
//		    .replaceAll("\"", "\\\"")
//		    .replaceAll("\r", "\\r")
//		    .replaceAll("\n", "\\n");
		  if(str.contains("\"")){
		  String replaced = str.replaceAll("\"", "");
		  return replaced;
		  }

		  
		  return str;
	  }
	  public void run(String consumerKey, String consumerSecret, String token, String secret) throws InterruptedException {
		  
		  parseconfiguration();
		  
	    // Create an appropriately sized blocking queue
	    BlockingQueue<String> queue = new LinkedBlockingQueue<String>(10000);
	    BasicClient client = null;
	  //StatusesSampleEndpoint endpoint = new StatusesSampleEndpoint();
	    StatusesFilterEndpoint endpoint = new StatusesFilterEndpoint();
	    
	    // Define our endpoint: By default, delimited=length is set (we need this for our processor)
	    // and stall warnings are on.
	    //StatusesSampleEndpoint endpoint = new StatusesSampleEndpoint();
	    //StatusesFilterEndpoint endpoint = new StatusesFilterEndpoint();
	    //endpoint.trackTerms(Lists.newArrayList("canada travel", "travel", "dream cruise", "cruise", "air travel"));
	    
	    endpoint.trackTerms(Lists.newArrayList(populateTwitterfields("key-words", " ")));
	    
	    endpoint.languages(Lists.newArrayList(populateTwitterfields("language", "en")));
	    //endpoint.locations(Lists.newArrayList(populateTwitterfields("location", "singapore")));
	    //endpoint.locations(Lists.newArrayList(populateTwitterfields("locations", "-124.85, 24.39, -66.88, 49.38,")));
	    Authentication auth = new OAuth1(consumerKey, consumerSecret, token, secret);
	    // Authentication auth = new BasicAuth(username, password);
	    
	    Location geo = new Location(new Coordinate (-124.85, 24.39), new Coordinate (-66.88, 49.38));
	    ArrayList<Location> myloc = new ArrayList<Location>();
	    myloc.add(geo);
	    //endpoint.locations(myloc);
	    // Create a new BasicClient. By default gzip is enabled.
	    
	    try{
	    	client = new ClientBuilder()
	      .hosts(Constants.STREAM_HOST)
	      .endpoint(endpoint)
	      .authentication(auth)
	      .processor(new StringDelimitedProcessor(queue))
	      .build();

	    // Create an executor service which will spawn threads to do the actual work of parsing the incoming messages and
	    // calling the listeners on each message
	    
	    int numProcessingThreads = 4;
	    ExecutorService service = Executors.newFixedThreadPool(numProcessingThreads);

	    // Wrap our BasicClient with the twitter4j client
	    //Twitter4jStatusClient t4jClient = new Twitter4jStatusClient(
	      //client, queue, Lists.newArrayList(listener1, listener2), service);
	    
	    Twitter4jStatusClient t4jClient = new Twitter4jStatusClient(
	  	      client, queue, Lists.newArrayList(listener2), service);
	    
	    // Establish a connection
	    t4jClient.connect();
	    for (int threads = 0; threads < numProcessingThreads; threads++) {
	    //while(!t4jClient.isDone()){
	      // This must be called once per processing thread
	     
	      t4jClient.process();
	      logger.info("Successfully logged in !");
	    }
		  //
		  //Thread s3stub = new Thread(new AudienceObject(myCategory, mySubcategory));
		  //s3stub.start();
	  }
	    catch(Exception e)
	    {
	    	logger.error(e);
	    	client.stop();
	    }
	  }
	
	  public static void main(String[] args) {
		  
		    try {
		    	
		    	logger.info("Attempting to connect !");
		    	TwitterEnterpriseStream obj  = new TwitterEnterpriseStream();
		    	obj.run(args[0], args[1], args[2], args[3]);
		    } catch (InterruptedException e) {
		      System.out.println(e);
		    }
		  }

}
