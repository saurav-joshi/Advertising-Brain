/**
 * Copyright 2013 Twitter, Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 **/

package com.saurav.Twitter.DataSerializer;

import com.google.common.collect.Lists;
import com.twitter.hbc.ClientBuilder;
import com.twitter.hbc.core.Client;
import com.twitter.hbc.core.Constants;
import com.twitter.hbc.core.endpoint.StatusesFilterEndpoint;
import com.twitter.hbc.core.processor.StringDelimitedProcessor;
import com.twitter.hbc.httpclient.auth.Authentication;
import com.twitter.hbc.httpclient.auth.OAuth1;
import com.twitter.hbc.twitter4j.parser.JSONObjectParser;

import twitter4j.JSONException;
import twitter4j.JSONObject;

import java.util.List;
import java.util.ArrayList;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class TwitterFilterStream {

  public static  void run(String consumerKey, String consumerSecret, String token, String secret) throws InterruptedException {
    BlockingQueue<String> queue = new LinkedBlockingQueue<String>(10000);
    List<String> tweetsbucket = new ArrayList<String>();
    StatusesFilterEndpoint endpoint = new StatusesFilterEndpoint();
  
    // add some track terms
    endpoint.trackTerms(Lists.newArrayList("canada travel", "#travel", "dreamcruise", "cruise", "air travel"));
    
    Authentication auth = new OAuth1(consumerKey, consumerSecret, token, secret);
    
    // Authentication auth = new BasicAuth(username, password);

    // Create a new BasicClient. By default gzip is enabled.
    Client client = new ClientBuilder()
            .hosts(Constants.STREAM_HOST)
            .endpoint(endpoint)
            .authentication(auth)
            .processor(new StringDelimitedProcessor(queue))
            .build();

    // Establish a connection
    client.connect();
    
    while (!client.isDone()){	
       //String msg = queue.take();
      //String msg = queue.poll(90, TimeUnit.SECONDS);
      
      if (queue.isEmpty()) {
    	  synchronized (client) {
    		    client.wait(60000);
    		}
    	  System.out.println(queue.size());
    	  System.out.println("After 1 min wait ");
    	  //client.wait(90);
    	  queue.clear();
          //System.out.println("Did not receive a message in 90 seconds");
          //break;
        } else {
        	System.out.println(queue.size());
        	
//          try {
//        	  //Clone the queue and release it for further processing 
//        	  queue.drainTo(tweetsbucket);
//        	  //Create a new thread we will pull this from thread pool later.... 
//        	  
//        	  //System.out.println(msg);
//			JSONObject json = new JSONObject(msg);
//			String text = json.getString("text");
//			JSONObject jUser = json.getJSONObject("user");
//			String languageTweet = jUser.getString("lang");
//			System.out.println(text);
//		} catch (JSONException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}

          //System.out.println(msg);
        }
    }

    //client.stop();

  }

  public static void main(String[] args) {
    try {
    	TwitterFilterStream.run(args[0], args[1], args[2], args[3]);
    } catch (InterruptedException e) {
      System.out.println(e);
    }
  }
}
