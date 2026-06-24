class copy_array
{
	public static void main(String args[])
	{
	  int arr[]={1,2,3,4,5};
	  int copy[]= arr.clone();
	  System.out.println("copied array");
	  for(int i:copy)
		{
	          System.out.print(i);
  		}
	}
}