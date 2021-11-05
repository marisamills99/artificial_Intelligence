public class ClassNameHere {
   public static void main(String[] args) {
      // ugly java program to trace the backtrack tree of a CSP
// Copyright Poole, Mackworth, Goebel, 1998


    for (int a =1 ; a <= 4; a++ ) {
       System.out.print("A="+a+" ");
       
       for (int b =1 ; b <= 4; b++ ) {
          if (b != 1) System.out.print("    ");
          System.out.print("B="+b+" ");
          for (int c =1 ; c <= 4; c++ ) {
             if (c != 1) System.out.print("        ");
             System.out.print("C="+c+" ");
             if (c != a && b!=c) {
                for (int d =1 ; d <= 4; d++ ) {
                   if (d != 1) System.out.print("            ");
                   System.out.print("D="+d+" ");
                   if (c != d && c!=d+1 && a>d) {
                       for (int e =1 ; e <= 4; e++ ) {
                        if (e != 1) System.out.print("                ");
                         System.out.print("E="+e+" ");
                         if ( d>e && c>e) {
     	                     System.out.println("success");
                         }
                         else 
	                System.out.println("failure");
		       }}
                 else 
	           System.out.println("failure");
		}}
             else 
	       System.out.println("failure");
				  
          }
       }
       
    
    }

   }
}