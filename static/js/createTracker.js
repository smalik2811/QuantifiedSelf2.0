new Vue({
    el: "#app",
    delimiters: ['${','}'],
    data(){
        return {
            userData: {
                name: null,
            },
            trackerData: {
                name: null,
                description: null,
                type: null,
                options: null,
            },

            trackerTypes: {
                "Numerical": 1,
                "Time Duration": 2,
                "Boolean": 3,
                "Multiple Choice": 4,
            },

            misc: {
                tr_type: null,
                options: null
            }
        }
    },

    methods: {

        selectType: function(type){
            if (type in this.trackerTypes){
                this.trackerData.type = this.trackerTypes[type]
                this.misc.tr_type = type
                
                if (this.trackerData.type == 4){
                    this.misc.options = "Option1, Option2, Option3"
                }else{
                    this.misc.options = null
                }
            }
        },

        userLogout(){
            fetch('/api/user/logout', {
                method: 'get',
                headers: {
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                },
            })
            .then((response) => 
            {
                localStorage.clear()
                document.cookie = 'my_cookie=; path=/; domain=http://192.168.139.50:8080/; expires=' + new Date(0).toUTCString();
                window.location.href = '/login';
            }) 
        },

        async createTracker(){

            if (this.misc.options != null){
                this.trackerData.options = this.misc.options.split(", ")
            }

            fetch('/api/tracker', {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                },
                body: JSON.stringify(this.trackerData),
            })
            .then((resopnse) => resopnse.json())
            .then((data) => 
                {
                    window.location.href = '/';
                })
                .catch((err) =>{
                    this.c.err = true;
                    this.c.errmsg = "Network error " + err;
                })
        }
    },

    computed: {
        multiChoice(){
          return this.trackerData.type === 4
      }
    },

    created() {
        fetch('/api/user', {
            method: 'get',
            headers: {
                'Authentication-Token': localStorage.getItem('Authentication-Token'),
            },
        })
        .then((response) => response.json())
        .then((user) => {
            this.userData.name = user.first_name,
            this.userData.name = this.userData.name + " " + user.last_name
        })
    },
});