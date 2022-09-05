new Vue({
    el: "#app",
    delimiters: ['${','}'],
    data(){
        return {
            formData: {
                email: '',
                password: '',
            },
        }
    },

    methods: {
        async loginUser(){
                fetch('/api/user/login?include_auth_token', {
                    method: 'post',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.formData),
                })
                .then((resopnse) => resopnse.json())
                .then((data) => 
                    {
                        localStorage.setItem(
                            'Authentication-Token',
                            data.response.user.authentication_token
                        )
                        window.location.href = '/';
                    })
                    .catch((err) =>{
                        this.c.err = true;
                        this.c.errmsg = "Network error " + err;
                    })
            }
    },
});