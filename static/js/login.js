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
                let response = await fetch('/api/user/login?include_auth_token', {
                                        method: 'post',
                                        headers: {
                                            'Content-Type': 'application/json',
                                        },
                                        body: JSON.stringify(this.formData),
                                    })
                
                if (response.status === 200) {
                    let data = await response.json();
                    localStorage.setItem(
                        'Authentication-Token',
                        data.response.user.authentication_token
                    )
                    window.location.href = '/';
                }else if (response.status === 400){
                    window.alert('Please check your credentials.')
                }else if (response.status === 500){
                    window.alert('Something went wrong.')
                }else{
                    window.alert(response.statusText)
                }
            }
    },

    created() {
        if (localStorage.getItem('Authentication-Token') != null){
            window.alert("You are already logged in.\nRedirecting to Home page.")
            window.location.href = '/'
        }
    }
});