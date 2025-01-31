var numComp = {  
    props:{
        logvalue: null,
    },  
    template: 
    `
        <div>
            <label class="form-label">Value</label>
            <input
                v-model="trackerValue"
                @input="$emit('sendvalue', trackerValue);"
                class="form-control"
                type="number"
                required="true"/>
        </div>
    `,
    data(){
        return {
            trackerValue: this.logvalue,
        }
    },
}

var timeComp = {   
    props:{
        logvalue: null,
    }, 
    template: 
    `
        <div>
            <label class="form-label">Value</label>
            <div class="mb-3 row">
                <div class="col-sm-10">
                    <input v-model="hour" @input="$emit('sendvalue', getValue);" type="range" min="0" max="12" value="0" required="true" class="form-range">
                </div>
                <label class="col-sm-2 col-form-label"><strong>{{hour}}</strong> Hours</label>
            </div>
            <div class="mb-3 row">
                <div class="col-sm-10">
                    <input v-model="minute" @input="$emit('sendvalue', getValue);" type="range" min="0" max="59" required="true" value="0"class="form-range">
                </div>
                <label class="col-sm-2 col-form-label"><strong>{{minute}}</strong> Minutes</label>
            </div>
        </div>
    `,
    data(){
        return {
            hour: parseInt(this.logvalue) / 60,
            minute: parseInt(this.logvalue) % 60,
        }
    },

    computed: {
        getValue(){
            return 60 * parseInt(this.hour) + parseInt(this.minute)
        },
    },
}

var boolComp = {    
    props:{
        logvalue: null,
    }, 
    template: 
    `
        <div>
            <label class="form-label">Value</label>
            <div class="form-check">
                <input class="form-check-input" required="true" type="radio" name="options" id="trueOption" value="true" v-model="trackerValue" @input="$emit('sendvalue', 'true');">
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
            trackerValue: this.logvalue,
        }
    },
}

var multiComp = {  
    props:{
        options: null,
        logvalue: null,
    },
    template: 
    `
        <div>
            <label class="form-label">Value</label>
            <div v-for="option in options">
                <div class="form-check">
                    <input class="form-check-input" required="true" type="radio" name="trackeroptions" :id="option" :value="option" v-model=trackerValue @input="$emit('sendvalue', option);">
                    <label class="form-check-label" :for="option">
                        {{option}}
                    </label>
                </div>
            </div>
        </div>
    `,
    data(){
        return {
            trackerValue: this.logvalue,
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
                id: null,
                value: null,
                note: null,
                timestamp: null,
                tracker_id: null,
            },
            userData: {
                name: null,
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

        async updateLog(){
            const log = {
                'value': this.logData.value,
                'timestamp': this.logData.timestamp.substring(0,10) + " " + this.logData.timestamp.substring(11,16),
                'note': this.logData.note
            }
            fetch('/api/log/' + this.logData.id, {
                method: 'patch',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': localStorage.getItem('Authentication-Token'),
                },
                body: JSON.stringify(log),
            })
            .then((response) => {
                if(response.status == 201){
                    window.location.href= "/summary/" + this.logData.tracker_id
                }else if(response.status == 400){
                    window.alert(response.statusText)
                }else if(response.status == 401){}
                else if(response.status == 404){
                    window.alert(response.statusText)
                }else if(response.status == 409){
                    window.alert(response.statusText)
                }else{
                    window.alert(response.statusText)
                }    
            })
        }    
    },

    async created() {
        // Fetching user details
        let response = await fetch('/api/user', {
            method: 'get',
            headers: {
                'Authentication-Token': localStorage.getItem('Authentication-Token'),
            },
        })
        if(response.status == 200){
            const user = await response.json()
            this.userData.name = user.first_name,
            this.userData.name = this.userData.name + " " + user.last_name
        }else if(response.status == 401){}
        else{
            window.alert("Something went wrong.")
            userLogout()
        }

        // Fetching log details
    
        let uri = window.location.pathname.split("/")
        this.logData.id = uri[uri.length - 1]
        
        response = await fetch('/api/log/' + this.logData.id, {
            method: 'get',
            headers: {
                'Authentication-Token': localStorage.getItem('Authentication-Token'),
            },
        })
        if(response.status == 200){
            let data = await response.json()
            this.logData = data
            let timestamp = this.logData.timestamp
            this.logData.timestamp = timestamp.substring(0,10) + "T" + timestamp.substring(11,16)
        }else if(response.status == 400){
            window.alert(response.statusText)
        }else if(response.status == 401){}
        else if(response.status == 404){
            window.alert(response.statusText)
        }else{
            window.alert(response.statusText)
        }

        // Fetch Tracker details
        response = await fetch('/api/tracker/' + this.logData.tracker_id, {
            method: 'get',
            headers: {
                'Authentication-Token': localStorage.getItem('Authentication-Token'),
            },
        })
        if(response.status == 200){
            data = await response.json()
            this.misc.tr_type = data.type
            this.misc.options = data.options
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
                    this.misc.options = data.options
                    break;
                default:
                    window.alert("Something went wrong.")
                    window.location.href="/"
                    break;
            }    
        }else if(response.status == 400){
            window.alert(response.statusText)
        }else if(response.status == 401){}
        else if(response.status == 404){
            window.alert(response.statusText)
        }else{
            window.alert(response.statusText)
        }        
    },
});