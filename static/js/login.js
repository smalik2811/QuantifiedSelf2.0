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
            const res = await fetch('/user/login?include_auth_token',{
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.formData),
            });

            if (res.ok){
                const data = await res.json()
                localStorage.setItem(
                    'Authentication-Token',
                    data.response.user.authentication_token
                )
                window.location.href = '/home';
            }
        }
    },
});