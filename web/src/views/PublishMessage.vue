<template>
  <div class="publishmessage">
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="标题" prop="title">
            <el-input v-model="ruleForm.title"></el-input>
        </el-form-item>
        <el-form-item label="内容" prop="content">
            <el-input type="textarea" v-model="ruleForm.content"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
            <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
        </el-form>
  </div>
</template>

<script>
import { AddMessage } from "@/common/api"
export default {
  name: 'PublishMessage',
  data() {
      return {
        ruleForm: {
          title: '',
          content: ''
        },
        rules: {
          title: [
            { required: true, message: '请输入标题名称', trigger: 'blur' },
            { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          content: [
            { required: true, message: '请填写内容', trigger: 'blur' }
          ]
        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
            AddMessage({title: this.ruleForm.title, content: this.ruleForm.content}).then(resp => {
                if (resp.err != null) {
                    alert(resp.msg)
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

