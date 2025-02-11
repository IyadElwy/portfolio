(function ($) {
    "use strict";

   
    $('#myTerminal').terminal(function(command, term) {
         if (command === 'clear'){
            term.clear();
        } else if (command !== '') {
            term.pause();
            fetch('https://portfolio.iyadelwy.xyz/cmd', {
                method: 'POST',
                body: JSON.stringify({command: command}),
                headers: {
                    "Content-Type": "application/json",
                  },
            }).then(function (response) {
                return response.json();
            }).then(function (data) {
                term.echo(data.result);
                term.resume()
            }).catch(function (err) {
                term.error("Network Error: Your command did not reach the host machine.");
                term.resume();
            });

        }
    }, {
        greetings: `
    ▗▖   ▄ ▄   ▄ ▗▞▀▚▖    ▗▖ ▗▖▄▄▄▄  ▄▄▄     ▗▄▄▖  ▄▄▄     ▐▌
    ▐▌   ▄ █   █ ▐▛▀▀▘    ▐▌▗▞▘█  █ ▀▄▄      ▐▌ ▐▌█   █    ▐▌
    ▐▌   █  ▀▄▀  ▝▚▄▄▖    ▐▛▚▖ █▀▀█ ▄▄▄▀     ▐▛▀▘ ▀▄▄▄▀ ▗▞▀▜▌
    ▐▙▄▄▖█                ▐▌ ▐▌█▄▄█          ▐▌         ▝▚▄▟▌
                                                                 
                                                                                                                           
You are currently in a Live Terminal Session running in multiple K8s Pods.\n\nThis environment was carefully designed to ensure robustness and security by running it on my own self-hosted Kubernetes Multi-Node cluster, running in my kitchen :)\n\nTo know more about how this environment was built check out the "Portfolio Projects" section bellow to access the project\'s GitHub.\n\nI also wrote a small Movie data CLI Tool and installed it into the pod so you don't get bored here.\nTo get started type "movies --help"\n\nP.S. Don't worry about breaking anything...Thanks to K8s, you can't.\n\n\n`,
        prompt: '> '
    });
    
})(jQuery);

