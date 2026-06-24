import java.io.*;

class a_in1
{
public static void main(String args[]) throws IOException
{
  InputStreamReader read= new InputStreamReader(System.in);
  BufferedReader in=new BufferedReader(read);
  int x,y,z;
  System.out.println("Enter the two numbers:");
  x=Integer.parseInt(in.readLine());
  y=Integer.parseInt(in.readLine());
  z=x+y;
  System.out.println("the sum of the number is="+z);
}
}
