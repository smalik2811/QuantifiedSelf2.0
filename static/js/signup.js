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
            if (this.confirm_password == this.userData.password){
                fetch('/api/user', {
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.userData),
                })
                .then((response) => {
                    if(response.status == 201){
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
            } else{
                    window.alert("Passwords entered do not match.")
            }
        }
    },
});