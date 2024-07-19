window.onload = function() {
      setTimeout(function() {
        var frame = document.getElementById('myFrame');
        frame.style.animation = "fade_out 1s forwards";
        setTimeout(function() {
          frame.style.display = "none";
        }, 1000);
      }, 500);
    };


        function no_come_go() {
            // body...
            document.getElementById('create_acc').style.transform = "scale(0.5, 0.5)"
            document.getElementById('create_acc').style.opacity = '0'
            document.getElementById('create_acc').style.borderRadius = '50%'
            document.getElementById('create_acc').style.top = '-100%'
        }
        function no_come_go_o() {
            // body...
            document.getElementById('del_acc').style.transform = "scale(0.5, 0.5)"
            document.getElementById('del_acc').style.top = '-100%'
            document.getElementById('del_acc').style.opacity = '0'
            document.getElementById('del_acc').style.borderRadius = '50%'
        }

        function de_func() {
            if (document.getElementById('del_acc_from_log').style.opacity == '1') {
                document.getElementById('del_acc_from_log').style.transform = "scale(0.5, 0.5)"
                document.getElementById('del_acc_from_log').style.top = '-100%'
                document.getElementById('del_acc_from_log').style.opacity = '0'
                document.getElementById('del_acc_from_log').style.borderRadius = '50%'
            }
            else {
                 document.getElementById('del_acc_from_log').style.transform = "scale(1, 1)"
                document.getElementById('del_acc_from_log').style.opacity = '1'
                document.getElementById('del_acc_from_log').style.top = '0%'
                document.getElementById('del_acc_from_log').style.borderRadius = '0%'
            }
        }

        function create_account() {
            if (document.getElementById('create_acc').style.opacity == '1') {
                document.getElementById('create_acc').style.transform = "scale(0.5, 0.5)"
                document.getElementById('create_acc').style.top = '-100%'
                document.getElementById('create_acc').style.opacity = '0'
                document.getElementById('create_acc').style.borderRadius = '50%'
            }
            else {
                 document.getElementById('create_acc').style.transform = "scale(1, 1)"
                document.getElementById('create_acc').style.opacity = '1'
                document.getElementById('create_acc').style.top = '0%'
                document.getElementById('create_acc').style.borderRadius = '0%'
            }
        }


        function fill_money(){
            if (document.getElementById('fill_acc').style.opacity == '1') {
                document.getElementById('fill_acc').style.transform = "scale(0.5, 0.5)"
                document.getElementById('fill_acc').style.top = '-100%'
                document.getElementById('fill_acc').style.opacity = '0'
                document.getElementById('fill_acc').style.borderRadius = '50%'
            }
            else{
                document.getElementById('fill_acc').style.transform = "scale(1, 1)"
                document.getElementById('fill_acc').style.opacity = '1'
                document.getElementById('fill_acc').style.top = '0%'
                document.getElementById('fill_acc').style.borderRadius = '0%'

            }
        }

        function transfer_money(){
            if (document.getElementById('transfer_acc').style.opacity == '1') {
                document.getElementById('transfer_acc').style.transform = "scale(0.5, 0.5)"
                document.getElementById('transfer_acc').style.top = '-100%'
                document.getElementById('transfer_acc').style.opacity = '0'
                document.getElementById('transfer_acc').style.borderRadius = '50%'
            }
            else{
                document.getElementById('transfer_acc').style.transform = "scale(1, 1)"
                document.getElementById('transfer_acc').style.opacity = '1'
                document.getElementById('transfer_acc').style.top = '0%'
                document.getElementById('transfer_acc').style.borderRadius = '0%'

            }
        }

        function withdraw_money(){
            if (document.getElementById('withdraw_acc').style.opacity == '1') {
                document.getElementById('withdraw_acc').style.transform = "scale(0.5, 0.5)"
                document.getElementById('withdraw_acc').style.top = '-100%'
                document.getElementById('withdraw_acc').style.opacity = '0'
                document.getElementById('withdraw_acc').style.borderRadius = '50%'
            }
            else{
                document.getElementById('withdraw_acc').style.transform = "scale(1, 1)"
                document.getElementById('withdraw_acc').style.opacity = '1'
                document.getElementById('withdraw_acc').style.top = '0%'
                document.getElementById('withdraw_acc').style.borderRadius = '0%'

            }
        }

    function pop_op_p(){
            if (document.getElementById('get_accounts').style.opacity == '1') {
                document.getElementById('get_accounts').style.transform = "scale(0.5, 0.5)"
                document.getElementById('get_accounts').style.top = '-100%'
                document.getElementById('get_accounts').style.opacity = '0'
                document.getElementById('get_accounts').style.borderRadius = '50%'
            }
            else{
                document.getElementById('get_accounts').style.transform = "scale(1, 1)"
                document.getElementById('get_accounts').style.opacity = '1'
                document.getElementById('get_accounts').style.top = '0%'
                document.getElementById('get_accounts').style.borderRadius = '0%'

            }
        }