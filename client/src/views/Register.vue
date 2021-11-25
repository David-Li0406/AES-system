<template>
    <div class="reg-container">
        <el-form ref="registerForm" :model="form" status-icon :rules="rules" label-width="0" class="register-box">
            <h3 class="register-title">{{$t('Register.title')}}</h3>
            <el-form-item prop="email">
                <el-input type="text" :placeholder="$t('Register.email')" v-model="form.email"></el-input>
            </el-form-item>
			<el-form-item prop="verificationCode">
                <el-input type="text" :placeholder="$t('Register.plsVerify')" v-model="form.verificationCode" style="width: 60%; float:left"></el-input>
                <el-button @click="send" style="width: 40%" type="success" :disabled="disabled=!show">
					<i class=" el-icon-mobile-phone" style="margin-left:-15px"></i>
                    <span v-show="show" class="verify-box">{{$t('Register.verify')}}</span>
                     <span v-show="!show" class="count">{{count}} s</span>
                </el-button>
            </el-form-item>
            <el-form-item prop="username">
                <el-input type="text" :placeholder="$t('Register.username')" v-model="form.username"></el-input>
            </el-form-item>
            <el-form-item prop="password">
                <el-input type="password" :placeholder="$t('Register.password')" v-model="form.password"></el-input>
            </el-form-item>
            <el-form-item prop="confirmPassword">
                <el-input type="password" :placeholder="$t('Register.confirmpw')" v-model="form.confirmPassword"></el-input>
            </el-form-item>
            <el-form-item prop="name">
                <el-input type="text" :placeholder="$t('Register.Uname')" v-model="form.name"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button class="return-button" @click="backToLogin">{{$t('Register.back')}}</el-button>
                <el-button type="primary" class="register-button" @click="onSubmit('registerForm')">{{$t('Register.Reg')}}</el-button>
            </el-form-item>
        </el-form>

        <el-dialog
            :title="$t('Register.hint')"
            :visible.sync="dialogVisible"
            width=30%>
            <span>{{$t('Register.WrongInp')}}</span>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="dialogVisible = false">{{$t('Register.Ok')}}</el-button>
            </span>
        </el-dialog>

        <el-dialog
            :title="$t('Register.hint')"
            :visible.sync="dialogVisible1"
            width=30%>
            <span>{{$t('Register.uReged')}}</span>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="dialogVisible1 = false">{{$t('Register.Ok')}}</el-button>
            </span>
        </el-dialog>

        <el-dialog
            :title="$t('Register.hint')"
            :visible.sync="dialogVisible2"
            width=30%>
            <span>{{$t('Register.eReged')}}</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible2 = false">{{$t('Register.Ok')}}</el-button>
                <el-button type="primary" @click="backToLogin">{{$t('Register.retLogIn')}}</el-button>
            </span>
        </el-dialog>

        <el-dialog
            :title="$t('Register.hint')"
            :visible.sync="dialogVisible3"
            width=30%
            @close="backToLogin">
            <span>{{ countMessage }}</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="backToLogin">{{$t('Register.ret')}}</el-button>
            </span>
        </el-dialog>
		
		<el-dialog
            :title="$t('Register.hint')"
            :visible.sync="dialogVisible4"
            width=30%>
            <span>{{$t('Register.v_message')}}</span>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="dialogVisible4 = false">{{$t('Register.Ok')}}</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import https from '../api/https.js'
	const TIME_COUNT = 60; // 更改倒计时时间

    export default {
        name: 'Register',
        data () {
			title:this.$t('Register.title');
			options:[
				{
					value: 'cn',
					label: '中文'
				},{
					value: 'en',
					label: 'English'
				},
			];
            // 修改密码后重新调用确认密码验证
            var validatePassword = (rule, value, callback) => {
                if (this.form.confirmPassword !== '') {
                    this.$refs.registerForm.validateField('confirmPassword');
                }
                callback();
            };
            // 判断确认密码与原密码是否一致的方法
            var validateConfirmPassword = (rule, value, callback) => {
                if (value !== this.form.password) {
                    callback(new Error(this.$t('Register.newerror')));
                } else {
                    callback();
                }
            };
            return {
				show: true, // 初始启用按钮
                count: '', // 初始化次数
                timer: null,
                form: {
                    email: '',
                    username: '',
                    password: '',
                    confirmPassword: '',
                    name: '',
					verificationCode: ''
                },
                dialogVisible: false,
                dialogVisible1: false,
                dialogVisible2: false,
                dialogVisible3: false,
				dialogVisible4: false,
                countMessage: '',
                interval: null,
                rules: {
                    email: [
                        {required: true, message: this.$t('Register.e_message1'), trigger: 'blur'},
                        {type: 'email', message: this.$t('Register.e_message2'), trigger: 'blur'}
                    ],
                    username: [
                        {required: true, message: this.$t('Register.u_message1'), trigger: 'blur'},
                        {min: 0, max: 20, message: this.$t('Register.u_message2'), trigger: ['blur', 'change']}
                    ],
                    password: [
                        {required: true, message: this.$t('Register.p_message1'), trigger: 'blur'},
                        {min: 8, max: 15, message: this.$t('Register.p_message2'), trigger: 'blur'},
                        {validator: validatePassword, trigger: 'blur'}
                    ],
                    confirmPassword: [
                        {required: true, message: this.$t('Register.confirm_password'), trigger: 'blur'},
                        {validator: validateConfirmPassword, trigger: 'blur'}
                    ],
                    name: [
                        {min: 0, max: 20, message: this.$t('Register.n_message'), trigger: ['blur', 'change']}
                    ],
					 verificationCode: [
                        {required: true, message: this.$t('Register.plsVerify'), trigger: 'blur'}
                    ]
                }
            }
        },
        methods: {
            onSubmit (formName) {
                var email = this.form['email'];
                var username = this.form['username'];
                var password = this.form['password'];
                var name = this.form['name'];
				var verificationCode = this.form['verificationCode'];
                var registerInfo = {
                    'email': email,
                    'username': username,
                    'password': password,
                    'name': name,
					'verificationCode': verificationCode
                    };

                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        https.fetchPost('register', registerInfo).then((res) => {
                            if (res.data['code'] === 200) {
                                // 倒计时5秒返回登录
                                let that = this;
                                let count = 5;
                                this.interval = window.setInterval(() => {
                                    that.countMessage = this.$t('Register.Successful_Reg') + count + this.$t('Register.BackLogIn');
                                    if (that.dialogVisible3 === false) {
                                        this.dialogVisible3 = true;
                                    }
                                    count--;
                                    if (count < 0) {
                                        window.clearInterval(that.interval);
                                        this.$router.push('/login');
                                    }
                                }, 1000);
                                return true;
                            } else {
                                // 邮箱已被注册显示dialog2
                                if (res.data['wrongType'] === 'email') {
                                    this.dialogVisible2 = true;
                                    return false;
                                // 用户名已被注册显示dialog1
                                } else if (res.data['wrongType'] === 'username') {
                                    this.dialogVisible1 = true;
                                    return false;
                                // 验证码不正确显示dialog4
                                } else if (res.data['wrongType'] === 'verificationCode') {
                                    this.dialogVisible4 = true;
                                    return false;
                                }
                            }
                        });
                    } else {
                        this.dialogVisible = true;
                        return false;
                    }
                });
            },
            backToLogin () {
                // 清空倒计时返回
                if (this.interval) {
                    window.clearInterval(this.interval);
                }
                this.$router.push('/login');
            }, 
			send () {
                if (!this.timer) {
                    this.count = TIME_COUNT;
                    this.show = false;
                    this.timer = setInterval(() => {
                        if (this.count > 0 && this.count <= TIME_COUNT) {
                            this.count--;
                        } else {
                            this.show = true;
                            clearInterval(this.timer); // 清除定时器
                            this.timer = null;
                        }
                    }, 1000)
                }
                https.fetchPost('confirm', {'email': this.form['email']}).then((res) => {
                    if (res.data['code'] === 200) {
                        return true;
                    } else {
                        if (res.data['wrongType'] === 'email') {
                                this.dialogVisible2 = true;
                        }
                        return false;
                    }
                })
            }
        }
    }
</script>

<style lang="scss" scoped>
	.reg-container {
        width: 100%;
        height: 100%;
        background: url(../assets/c.png) center center no-repeat;
        background-size: 100% 100%;
		position:fixed;
        background-attachment: fixed;
		overflow: auto;
		z-index: -1;
    }
    .register-box {
        border: 1px solid #DCDFE6;
        width: 350px;
        margin: 142px auto;
        padding: 25px 35px 30px 35px;
        border-radius: 5px;
        -webkit-border-radius: 5px;
        box-shadow: 0 0 25px #909399;
    }
    .register-title {
        text-align: center;
        margin: 0 auto 20px auto;
        color: #303133;
    }
    .return-button {
        position: absolute;
        left: 10px;
    }
	.verify-box{
		font-size:12px;
	}
    .register-button {
        position: absolute;
        right: 10px;
    }
</style>
