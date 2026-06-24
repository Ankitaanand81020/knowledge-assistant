import java.io.*;
class a_in2
{
public static void main(String args[]) throws IOException
{ 
  int x;
  double t;
  InputStreamReader read=new InputStreamReader(System.in);
  BufferedReader in=new BufferedReader(read);
  System.out.println("enter a number:");
  x=Integer.parseInt(in.readLine());
  t=Math.sqrt(x);
  System.out.println("Square root is="+t);
}} 
  