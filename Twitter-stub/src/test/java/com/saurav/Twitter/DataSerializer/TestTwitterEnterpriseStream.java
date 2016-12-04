package com.saurav.Twitter.DataSerializer;

import static org.junit.Assert.*;

import org.junit.Test;

//import junit.framework.Test;
//import junit.framework.TestCase;
//import junit.framework.TestSuite;


/**
 * Unit test for simple App.
 */
public class TestTwitterEnterpriseStream 
    //extends TestCase
{
//    /**
//     * Create the test case
//     *
//     * @param testName name of the test case
//     */
//    public TestTwitterEnterpriseStream( String testName )
//    {
//        super( testName );
//    }
//
//    /**
//     * @return the suite of tests being tested
//     */
//    public static Test suite()
//    {
//        return new TestSuite( TwitterEnterpriseStream.class );
//    }

    /**
     * Rigourous Test :-)
     */
@Test
    public void testApp()
    { 
    	TwitterEnterpriseStream obj = new TwitterEnterpriseStream();
        //System.out.println(obj.createAudienceMsg("How cool is \"not\" these Dutch"));
        System.out.println(obj.createAudienceMsg("How cool is \"not\" these Dutch"));
        assertEquals("How cool is not these Dutch", obj.createAudienceMsg("How cool is \"not\" these Dutch") );
    }
}
