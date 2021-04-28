<template>
  <div class="authlogin">
    <div class="panel">
        <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
            <el-form-item label="用户名" prop="username">
                <el-input v-model="ruleForm.username"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="pass">
                <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                <el-button @click="resetForm('ruleForm')">重置</el-button>
            </el-form-item>
        </el-form>
    </div>
  </div>
</template>

<script>
import { LoginAPI } from "@/common/api"
export default {
  name: 'AuthLogin',
  data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.ruleForm.checkPass !== '') {
            this.$refs.ruleForm.validateField('checkPass');
          }
          callback();
        }
      };
      return {
        ruleForm: {
          username: '',
          pass: '',
        },
        rules: {
          username: [
            { message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            LoginAPI({username: this.ruleForm.username, password: this.ruleForm.pass}).then(resp => {
                if (resp.err != null) {
                    alert(resp.msg)
                } else {
                    this.$router.push({path: '/'})
                }
            })
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
}
</script>

<style scoped>
    .authlogin {
        padding-top: 160px;
    }
    .panel {
        width: 500px;
        margin: auto;
        background-color: #fff;
        padding-top: 40px;
        padding-right: 40px;
        padding-bottom: 20px;
        border-radius: 5px;
    }
</style>
