var numComp = {    
    template: 
    `
        <div>
            <label class="form-label">Value</label>
            <input
                v-model="trackerValue"
                @input="$emit('sendvalue', trackerValue);"
                class="form-control"
                type="number"/>
        </div>
    `,
    data(){
        return {
            trackerValue: null,
        }
    },
}

var timeComp = {    
    template: 
    `
        <div>
            <label class="form-label">Value</label>
            <div class="mb-3 row">
                <div class="col-sm-10">
                    <input v-model="hour" @input="$emit('sendvalue', getValue);" type="range" min="0" max="12" value="0" class="form-range">
                </div>
                <label class="col-sm-2 col-form-label"><strong>{{hour}}</strong> Hours</label>
            </div>
            <div class="mb-3 row">
                <div class="col-sm-10">
                    <input v-model="minute" @input="$emit('sendvalue', getValue);" type="range" min="0" max="59" value="0"class="form-range">
                </div>
                <label class="col-sm-2 col-form-label"><strong>{{minute}}</strong> Minutes</label>
            </div>
        </div>
    `,
    data(){
        return {
            hour: 0,
            minute: 0,
        }
    },

    computed: {
        getValue(){
            return 60 * parseInt(this.hour) + parseInt(this.minute)
        },
    },
}

var boolComp = {    
    template: 
    `
        <div>
            <label class="form-label">Value</label>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="options" id="trueOption" value="true" v-model="trackerValue" @input="$emit('sendvalue', 'true');">
                <label class="form-check-label" for="trueOption">
                    True
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="options" id="falseOption" value="false" v-model="trackerValue" @input="$emit('sendvalue', 'false');">
                <label class="form-check-label" for="falseOption">
                    False
                </label>
            </div>
        </div>
    `,
    data(){
        return {
            trackerValue: null
        }
    },
}

var multiComp = {    
    template: 
    `
        <div>
            <label class="form-label">Value</label>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="options" id="trueOption" value="true" v-model="trackerValue" @input="$emit('sendvalue', 'true');">
                <label class="form-check-label" for="trueOption">
                    True
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="options" id="falseOption" value="false" v-model="trackerValue" @input="$emit('sendvalue', 'false');">
                <label class="form-check-label" for="falseOption">
                    False
                </label>
            </div>
        </div>
    `,
    data(){
        return {
            trackerValue: null
        }
    },
}

let app = new Vue({
    el: "#app",
    delimiters: ['${','}'],
    components: {
        'num-comp': numComp,
        'time-comp': timeComp,
        'bool-comp': boolComp,
        'multi-comp': multiComp,
    },
    data(){
        return {
            valueComponent: null,
            logData:{
                value: null,
                note: null,
                timestamp: null,
            },
            userData: {
                name: null,
            },
            trackerData: {
                id: null,
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
        
        getvalue: function(value){
            this.logData.value = value
        },

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
            .then((response) => {
                if(response.status == 201){
                    return response.json()
                }else if(response.status == 400){
                    window.alert(response.statusText)
                }else if(response.status == 401){}
                else if(response.status == 409){
                    window.alert(response.statusText)
                }else{
                    window.alert(response.statusText)
                }
                
            })
            .then((data) => 
                {
                    window.location.href = '/';
                })
        }
    },

    computed: {
        multiChoice(){
          return this.trackerData.type === 4
      }
    },

    created() {
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
            this.userData.name = user.first_name,
            this.userData.name = this.userData.name + " " + user.last_name
        })

        // Fetching tracker details
        {
            let uri = window.location.pathname.split("/")
            this.trackerData.id = uri[uri.length - 1]

            fetch('/api/tracker/' + this.trackerData.id, {
                method: 'get',
                headers: {
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                },
            })
            .then((response) => {
                if(response.status == 200){
                    return response.json()
                }else if(response.status == 400){
                    window.alert(response.statusText)
                }else if(response.status == 401){}
                else if(response.status == 404){
                    window.alert(response.statusText)
                }else{
                    window.alert(response.statusText)
                }  
            })
            .then((data) => 
                {
                    this.misc.tr_type = data.type
                    this.trackerData.name = data.name
                    switch(this.misc.tr_type){
                        case 1:
                            this.valueComponent = 'num-comp'
                            break;
                        case 2:
                            this.valueComponent = 'time-comp'
                            break;
                        case 3:
                            this.valueComponent = 'bool-comp'
                            break;
                        case 4:
                            this.valueComponent = 'multi-comp'
                            break;
                        default:
                            window.alert("Something went wrong.")
                            window.location.href="/"
                    }
                }
            )
        }
      },
});