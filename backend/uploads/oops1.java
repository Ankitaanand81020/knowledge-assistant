import java.util.*;
class oops
{
 Scanner in=new Scanner(System.in);
 int x,y,z;
 void input()
 {
  System.out.println("enter the two numbers");
  x=in.nextInt();
  y=in.nextInt();
 }
  void process()
{
 z=x+y;
}
 void output()
{
  System.out.println("sum of the two numbers is ="+z);
 }
}
class oops1
{
 public static void main(String args[])
 {
  oops obj=new oops();
  obj.input();
  obj.process();
  obj.output();
 }
}