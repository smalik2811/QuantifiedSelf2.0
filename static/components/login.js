const login = {
    template: `
    <div class="container" style="padding: 20px;background: #ffffff;border-radius: 15px;margin-top: 15vh;">
        <div class="row">
            <div class="col-md-6" style="background: url(&quot;../static/img/computer.webp&quot;) center / contain no-repeat;">
                <div></div>
            </div>
            <div class="col-md-6" style="padding: 50px;">
                <div style="width: 300px;padding: 7px;">
                    <form action="/" method="POST" id="login-form">
                        <div>
                            <p style="font-size: 25px;font-weight: bold;">Member Login</p>
                        </div>
                        <div style="background: #f1f1f1;border-radius: 25px;padding: 10px;"><i class="fa fa-envelope" style="margin-left: 15px;color: rgb(152,152,152);"></i><input name = "user"  type="text" data-bss-hover-animate="pulse" style="background: rgba(255,255,255,0);border-style: none;margin-left: 10px;color: rgb(152,152,152);width: 220px;" placeholder="Username"></div>
                        <div style="background: #f1f1f1;border-radius: 25px;padding: 10px;margin-top: 15px;"><i class="fa fa-lock" style="margin-left: 15px;color: rgb(152,152,152);font-size: 20px;"></i><input  name = "pass" type="text" data-bss-hover-animate="pulse" style="background: rgba(255,255,255,0);border-style: none;margin-left: 10px;color: rgb(152,152,152);width: 220px;" placeholder="Password"></div>
                        <div style="background: #95e47a;border-radius: 25px;margin-top: 15px;"><button class="btn text-center" data-bss-hover-animate="pulse" type="submit" style="color: rgb(255,255,255);width: 286px;height: 58px;border-radius: 25px;">Login</button></div>
                        <div>
                            <p class="text-center" style="margin-top: 10px;color: rgb(152,152,152);">Create new account?&nbsp; &nbsp; <a href="/signup">Click here</a></p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>`
}

export default login