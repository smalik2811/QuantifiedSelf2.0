Vue.component('log', {
    props: {
        id: '',
        value: '',
        note: '',
        timestamp: '',
    },

    template:
        `
            <tr>
                <td>{{value}}</td>
                <td style="max-width: 22px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{{timestamp}}</td>
                <td style="max-width: 60px; text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{{note}}</td>
                <td>
                    <div>
                        <div class="dropdown">
                            <button class="btn btn-warning dropdown-toggle" aria-expanded="false" data-bs-toggle="dropdown" type="button">Action</button>
                            <div class="dropdown-menu">
                            <button @click="updateLog(id)"class="dropdown-item link-info" type="button"><strong>Update</strong></button>
                            <button @click="removeLog(id)" class="dropdown-item link-danger" type="button"><strong>Remove</strong></button>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
    `,

    created(){
        if (localStorage.getItem('Authentication-Token') == null){
            window.alert("You are not authorised.\nRedirecting to Login page.")
            window.location.href = '/login'
        }
    },

    methods:{
        async removeLog(id){
            fetch('/api/log/' + id,{
                method: 'delete',
                headers: {
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                },
            })
            .then((response) => {
                if(response.status == 200){
                    window.location = window.location
                }else if(response.status == 401){}
                else if(response.status == 404){
                    window.alert(response.statusText)
                }else{
                    window.alert("Something went wrong.")
                    vue.userLogout()
                }
            })
        },

        async updateLog(id){
            window.location.href = "/log/update/" + id
        }

    }
})

let vue = new Vue({
    el: "#app",
    delimiters: ['${','}'],
    data(){
        return {
            name: null,
            ctx: null,
            optionDict: {},
            labelDict: {},
            chartmeta: {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Logs',
                        data: [],
                        backgroundColor: "#4e73df",
                        borderColor: "#4e73df"
                    }]
                },
                options: null,
            },
            count: 0,
            logs: [],
            unit: null,
            loaded: false,
            trackerData: {
                id: null,
                name: null,
                description: null,
                type: null
            }
        }
    },

    methods: {
        getMonth(date){
            month = date.getMonth()+1
                if(month < 10){
                    month = "0" + month
                }
                return month
        },
        formatDate(date){
            date = new Date(date)
            strYear = date.getFullYear();
            strMonth = this.getMonth(date)
            strDay = date.getDate();
            strDate = strYear + "-" + strMonth + "-" + strDay;
            return strDate
        },
        loadToday(){
            this.chartmeta.data.labels = []
            this.chartmeta.data.datasets[0].data = []
            this.logs.forEach(element => {
                if(element.timestamp.substring(0,10) == this.formatDate(new Date())){
                    this.chartmeta.data.labels.push(element.timestamp)
                    this.chartmeta.data.datasets[0].data.push(element.value)
                }
            })
            myChart = new Chart(this.ctx, this.chartmeta);
        },
        loadWeek(){
            currentDate = new Date()
            weekFirstDate = new Date()
            weekFirstDate.setDate(currentDate.getDate() - currentDate.getDay())
            weekLastDate = new Date()
            weekLastDate.setDate(weekFirstDate.getDate() + 6)
            weekFirstDate = this.formatDate(weekFirstDate)
            weekLastDate = this.formatDate(weekLastDate)

            this.chartmeta.data.labels = []
            this.chartmeta.data.datasets[0].data = []
            this.logs.forEach(element => {
                if(weekFirstDate <= element.timestamp.substring(0,10) && element.timestamp.substring(0,10) <= weekLastDate){
                    this.chartmeta.data.labels.push(element.timestamp)
                    this.chartmeta.data.datasets[0].data.push(element.value)
                }
            })
            myChart = new Chart(this.ctx, this.chartmeta);
        },
        loadMonth(){
            this.chartmeta.data.labels = []
            this.chartmeta.data.datasets[0].data = []
            this.logs.forEach(element => {
                if(element.timestamp.substring(5,7) == this.getMonth(new Date())){
                    this.chartmeta.data.labels.push(element.timestamp)
                    this.chartmeta.data.datasets[0].data.push(element.value)
                }
            })
            myChart = new Chart(this.ctx, this.chartmeta);
        },
        async userLogout(){
            let response = await fetch('/api/user/logout', {
                                    method: 'get',
                                    headers: {
                                        'Authentication-Token': localStorage.getItem('Authentication-Token'),
                                    },
                                })
            if (response.status === 200) {
                localStorage.clear()
                window.location.href = '/login';
            }else if (response.status === 401){
                window.alert('You are now authorised.')
                window.location.href = '/login';
            }else if (response.status === 500){
                window.alert('Something went wrong.')
            }else{
                window.alert(response.statusText)
            } 
        },

        async fetchTracker(){
            let uri = window.location.pathname.split("/")
            this.trackerData.id = uri[uri.length - 1]
            await fetch('/api/tracker/' + this.trackerData.id,{
                method: 'get',
                headers: {
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                },
            })
            .then((response) => {
                if(response.status == 200){
                    return response.json()
                }else if(response.status == 401){}
                else{
                    window.alert("Something went wrong.")
                    userLogout()
                }
            })
            .then((tracker) => {
                this.trackerData.name = tracker.name
                this.trackerData.description = tracker.description
                this.trackerData.type = tracker.type
            });
        },

        async fetchLogs(){
    
            await fetch('/api/log',{
                method: 'get',
                headers: {
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                    'trackerid' : this.trackerData.id,
                },
            })
            .then((response) => {
                if(response.status == 200){
                    return response.json()
                }else if(response.status == 401){}
                else{
                    window.alert("Something went wrong.")
                    userLogout()
                }
            })
            .then((logs) => {
                this.logs = logs
                this.logs.sort((a,b) => {
                    if(a.timestamp.substring(0,10) < b.timestamp.substring(0,10)){
                        return -1
                    }else if (a.timestamp.substring(0,10) ==b.timestamp.substring(0,10)){
                        if(a.timestamp.substring(11,16) < b.timestamp.substring(11,16)){
                            return -1
                        }else{
                            return 1
                        }
                    }else{
                        return 1
                    }
                })
                switch(this.trackerData.type){
                    case 1:
                        this.chartmeta.options = {
                            maintainAspectRatio: true,
                            legend: {
                                display: false,
                                labels: {
                                    fontStyle: "normal"
                                },
                                reverse: false
                            },
                            title: {
                                fontStyle: "normal",
                                position: "top",
                                display: false,
                                text: "Your Progress"
                            },
                            scales: {
                                x: {
                                    ticks: {
                                        fontStyle: "normal",
                                    }
                                },
                                y: {
                                    ticks: {
                                        fontStyle: "normal",
                                        beginAtZero: true
                                    }
                                }
                            }
                        };
                        logs.forEach(element => {
                            this.chartmeta.data.labels.push(element.timestamp)
                            this.chartmeta.data.datasets[0].data.push(element.value)
                        })
                        break
                    case 2:
                        this.unit=" (mins)"
                        this.chartmeta.options = {
                            maintainAspectRatio: true,
                            legend: {
                                display: false,
                                labels: {
                                    fontStyle: "normal"
                                },
                                reverse: false
                            },
                            title: {
                                fontStyle: "normal",
                                position: "top",
                                display: false,
                                text: "Your Progress"
                            },
                            scales: {
                                x: {
                                    ticks: {
                                        fontStyle: "normal",
                                    }
                                },
                                y: {
                                    ticks: {
                                        fontStyle: "normal",
                                        beginAtZero: true
                                    }
                                }
                            }
                        };
                        logs.forEach(element => {
                            this.chartmeta.data.labels.push(element.timestamp)
                            this.chartmeta.data.datasets[0].data.push(element.value)
                        })
                        break
                    case 3:
                        this.chartmeta.type = "bar"
                        this.chartmeta.options = {
                            maintainAspectRatio: true,
                            legend: {
                                display: false,
                                labels: {
                                    fontStyle: "normal"
                                },
                                reverse: false
                            },
                            title: {
                                fontStyle: "normal",
                                position: "top",
                                display: false,
                                text: "Your Progress"
                            },
                            scales: {
                                y: {
                                    ticks: {
                                        fontStyle: "normal",
                                        callback: function(label, index, labels) {
                                            switch (label) {
                                              case -1:
                                                return 'False';
                                              case 1:
                                                return 'True';
                                            }
                                        }
                                    }
                                }
                            }
                        };
                        logs.forEach(element => {
                            this.chartmeta.data.labels.push(element.timestamp)
                            if(element.value == "false"){
                                this.chartmeta.data.datasets[0].data.push(-1)
                            }else{
                                this.chartmeta.data.datasets[0].data.push(1)
                            }
                        })
                        break
                    case 4:
                        this.chartmeta.type = "bar"
                        logs.forEach(element => {
                            this.chartmeta.data.labels.push(element.timestamp)
                            if(! this.optionDict[element.value]){
                                this.optionDict[element.value] = [this.count * 5 , this.count * 5 + 4]
                                this.labelDict[this.count] = element.value
                                this.count = this.count + 1
                            }
                            this.chartmeta.data.datasets[0].data.push(this.optionDict[element.value])
                        })
                        this.chartmeta.options = {
                            maintainAspectRatio: true,
                            legend: {
                                display: false,
                                labels: {
                                    fontStyle: "normal"
                                },
                                reverse: false
                            },
                            title: {
                                fontStyle: "normal",
                                position: "top",
                                display: false,
                                text: "Your Progress"
                            },
                            scales: {
                                y: {
                                    ticks: {
                                        min: 0,
                                        stepSize: 1,
                                        fontStyle: "normal",
                                        callback: function(value, index, ticks) {  
                                            console.log("#1 Value:" + value)  
                                            let num = value + 1 
                                            if((num % 5) == 0 && (num / 5) <= 2){
                                                console.log("#2 Value:" + value)
                                                return this.labelDict[num/5]
                                            }
                                        }
                                    }
                                }
                            }
                        };
                        break
                }
            });
        },

    },
    
    created() {
        // Redirect to login page if not authorised
        if (localStorage.getItem('Authentication-Token') == null){
            window.alert("You are not authorised.\nRedirecting to Login page.")
            window.location.href = '/login'
            return
        }

        // Fetching trackers to show in the dashboard.
        this.fetchTracker()
        this.fetchLogs()
        
        // Fetching user details
        fetch('/api/user', {
            method: 'get',
            headers: {
                'Authentication-Token': localStorage.getItem('Authentication-Token'),
            },
        })
        .then((response) => {
            if(response.status == 200){
                return response.json()
            }else if(response.status == 401){}
            else{
                window.alert("Something went wrong.")
                userLogout()
            }
        })
        .then((user) => {
            this.name = user.first_name,
            this.name = this.name + " " + user.last_name
        })
    },
    async mounted(){
        this.ctx = document.getElementById('myChart').getContext('2d');
        setTimeout(() => {
            new Chart(this.ctx, this.chartmeta)
           }, 1000);        
    },
});
