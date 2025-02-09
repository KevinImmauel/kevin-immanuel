import React from "react";

const TextArt = () => {
  const textArt = `
                                             
                                -+%@@#                   -+=:.                        
                   .=.         *@@@@@@%.                 *@@@@@%+                    
               .=*%@@%:         -@@@@@@@:                %@@@@@#.                    
               .%@@@@@@-         :@@@@@@@:              .@@@@@@-                     
                 #@@@@@@-         .%@@@@@@:             +@@@@@@                      
                  #@@@@@@-         .%@@@@@@:            @@@@@@+                      
                   *@@@@@@-         .%@@@%*-           =@@@@@@.                  kevinvcx@DESKTOP-YOURMOM                      
                    *@@@@@@-         .*=.             .@@@@@@+                   ------------------------                       
                     #@@@@@%.                         *@@@@@%                    OS: Kali GNU/Linux                       
                     .@@#=:                          -@@@@@@-                    Kernel: 19.6.2-Autonomic Nervous System                
                      .                             :@@@@@@*                     Uptime: 617,622,141 secs 
                                                   .@@@@@@#                      Packages: WebDev, IoT, AI/ML, Linux (dpkg) 
                                                  :@@@@@@%                       Shell: bash 5.2.32 
                                                 =@@@@@@%.                       Terminal: Alacritty
                                               .#@@@@@@#                         CPU: adv. biological neural engine 
                                             .+@@@@@@@=                          Memory: ~105 million MiB / ~10.5 billion MiB
                                           -#@@@@@@@*                                
                                        -*@@@@@@@@*.                                 
                                    .=#@@@@@@@@@+.                        
                               .-+#@@@@@@@@@@#-                                  
                         .-=*#@@@@@@@@@@@@*-                                 
                          =@@@@@@@@@@@#=:                                 
                           .*@@@@%*=.                                        
                             :-:                                    
  `;

  return (
      <pre className="whitespace-pre font-mono">{textArt}</pre>
  );
};

export default TextArt;
