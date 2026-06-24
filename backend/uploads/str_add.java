class str_add
{
 public static void main(String args[])
{
 String first = "java";
 System.out.println("first string " +first);
 String second="Programming";
 System.out.println("second string " +second);
 first=second.concat(first);
 System.out.println("Joined string " +first);
 }
}