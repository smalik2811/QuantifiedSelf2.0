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
                .then((resopnse) => resopnse.json())
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
});