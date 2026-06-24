import java.io.*;

class sum_1
{
    public static void main(String[] args) throws IOException {
        int a,b, c;

             DataInputStream input = new DataInputStream(System.in);

               System.out.print("Enter the two numbers: ");
               a = Integer.parseInt(input.readLine());
               b = Integer.parseInt(input.readLine());

               c = a + b;

               System.out.println("The sum is = " + c);
    }
}
