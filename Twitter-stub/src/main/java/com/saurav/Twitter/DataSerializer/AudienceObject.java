package com.saurav.Twitter.DataSerializer;

import static java.nio.file.StandardWatchEventKinds.ENTRY_CREATE;
import java.nio.file.FileSystems;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.WatchEvent;
import java.nio.file.WatchKey;
import java.nio.file.WatchService;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BlockingQueue;

import org.apache.log4j.Logger;

import java.io.File;
import java.io.IOException;

import com.amazonaws.AmazonClientException;
import com.amazonaws.AmazonServiceException;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.PutObjectRequest;

import twitter4j.JSONException;
import twitter4j.JSONObject;

public class AudienceObject implements Runnable {
	
	final static Logger logger = Logger.getLogger(AudienceObject.class);
	private final List<String> tweetsbucket = new ArrayList<String>();
	String myCategory;
	String  mySubcategory;
    public AudienceObject(BlockingQueue<String> queue)
    {
    	queue.drainTo(tweetsbucket);
    }
    
    public AudienceObject(String cat, String subcat) {
		// TODO Auto-generated constructor stub
    	myCategory =cat;
    	mySubcategory = subcat;
	}
       
    	public AudienceObject() {
		// TODO Auto-generated constructor stub
	}

		private static String bucketName     = "joshi_saurav";
    	private static String keyName        = "2B3raQ9JVlIkjGY8jC8Q1TTDWguxihgYUovTYiwG";
    	private static String uploadFileName = "./log/live-tweets.csv.1";
    	
    	private static void uploadtoS3(File file) throws IOException {
            AmazonS3 s3client = new AmazonS3Client(new ProfileCredentialsProvider());
            try {
            	logger.info("Uploading a new object to S3 from a file\n");
                //File file = new File(uploadFileName);
                s3client.putObject(new PutObjectRequest(
                		                 bucketName, keyName, file));

             } catch (AmazonServiceException ase) {
            	 logger.error("Caught an AmazonServiceException, which " +
                		"means your request made it " +
                        "to Amazon S3, but was rejected with an error response" +
                        " for some reason.");
            	 logger.error("Error Message:    " + ase.getMessage());
            	 logger.error("HTTP Status Code: " + ase.getStatusCode());
            	 logger.error("AWS Error Code:   " + ase.getErrorCode());
            	 logger.error("Error Type:       " + ase.getErrorType());
            	 logger.error("Request ID:       " + ase.getRequestId());
            } catch (AmazonClientException ace) {
            	logger.error("Caught an AmazonClientException, which " +
                		"means the client encountered " +
                        "an internal error while trying to " +
                        "communicate with S3, " +
                        "such as not being able to access the network.");
            	logger.error("Error Message: " + ace.getMessage());
            }
        }
    	public void run()
    	{
    		
    		try {
                WatchService watcher = FileSystems.getDefault().newWatchService();
                Path dir = Paths.get("./log"); 
                
                dir.register(watcher, ENTRY_CREATE);
                 
                logger.info("Watch Service registered for dir: " + dir.getFileName());
                
                 
                while (true) {
                    WatchKey key;
                    try {
                        key = watcher.take();
                    } catch (InterruptedException ex) {
                        return;
                    }
                                              
                    WatchEvent.Kind<?> kind =  ((WatchEvent<?>) key.pollEvents()).kind();
                     @SuppressWarnings("unchecked")
                     WatchEvent<Path> ev = (WatchEvent<Path>) key.pollEvents();
                     Path fileName = ev.context();
                         
                     logger.info(kind.name() + ": " + fileName);
                         
                     if (kind == ENTRY_CREATE &&
                                fileName.toString().equals("live-tweets.csv.1")) {
                    	 logger.info("My source file has changed!!!");
                            
                            File oldfile =new File(uploadFileName);
                    		File newfile =new File(myCategory + mySubcategory + System.currentTimeMillis()); 
                    		
                    		if(oldfile.renameTo(newfile)){
                    			logger.info("Rename succesful");
                    			uploadtoS3(newfile);
                    			
                    		}else{
                    			logger.info("Rename failed");
                    			uploadtoS3(oldfile);
                    		}
                        }
                    
                     
                    boolean valid = key.reset();
                    if (!valid) {
                    	logger.warn("Breaking out !!! :: has something gone wrong");
                        break;
                    }
                }
                 
            } catch (IOException ex) {
            	logger.error(ex);
            }
        }
    	
    	
    	
    
//    public void run()
//    {
//    	try {
//      	  //Clone the queue and release it for further processing 
//      	  //queue.drainTo(tweetsbucket);
//      	  //Create a new thread we will pull this from thread pool later.... 
//    		
//      	  //System.out.println(msg);
////			JSONObject json = new JSONObject(msg);
////			String text = json.getString("text");
////			JSONObject jUser = json.getJSONObject("user");
////			String languageTweet = jUser.getString("lang");
////			System.out.println(text);
//		} 
//    	//catch (JSONException e) {
//    	catch (Exception e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//    }
	public

	String text;
	List<String> hashtags;
	String language;
	String url;
	String anchorurl;
	String anchorurl_description;
	String handle;
	String creation_time;
	String location;
	String followers_count;
	String friends_count;
	String listed_count;
	String favourites_count;
	String statuses_count;
	

}
