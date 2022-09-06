new Vue({
    el: "#app",
    delimiters: ['${','}'],
    data(){
        return {
            userData: {
                firstName: '',
                lastName: '',
                email: '',
                password: '',
            },
            confirm_password: '',
        }
    },

    methods: {
        async signup(){
                fetch('/api/user', {
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.userData),
                })
                .then((response) => {
                    if(response.status == 200){
                        return response.json()
                    }else if(response.status == 400){
                        window.alert(response.statusText)
                    }else if(response.status == 409){
                        window.alert(response.statusText)
                    }
                    else{
                        window.alert("Something went wrong.")
                        userLogout()
                    }
                })
                .then((data) => 
                    {
                        window.location.href = '/login';
                    })
                    .catch((err) =>{
                        this.c.err = true;
                        this.c.errmsg = "Network error " + err;
                    })
            }
    },

    created() {
        // Redirect to login page if not authorised
        if (localStorage.getItem('Authentication-Token') == null){
            window.alert("You are not authorised.\nRedirecting to Login page.")
            window.location.href = '/login'
            return
        }
    }
});