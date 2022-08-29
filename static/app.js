import login from './components/login.js'

const routes = [
    {path: "/", component: login}
]

const router = new VueRouter({
    routes, 
    base: "/",
})

const app = new Vue({
    el: "#app",
    router
})