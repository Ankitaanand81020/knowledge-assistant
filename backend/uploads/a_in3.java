import java.io.*;
class a_in3
{
public static void main(String args[]) throws IOException
{ 
try
{
  int a,b,c;

  DataInputStream in =new DataInputStream(System.in);
  System.out.println("enter the two numbers:");
  a=Integer.parseInt(in.readLine());
  b=Integer.parseInt(in.readLine());
  c=a+b;
  System.out.println("the sum is="+c);
}
 