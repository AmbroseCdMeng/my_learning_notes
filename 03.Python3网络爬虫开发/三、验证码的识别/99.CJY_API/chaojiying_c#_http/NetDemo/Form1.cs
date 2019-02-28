using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using System.IO;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace NetDemo
{
    public partial class Form1 : Form
    {
        public byte[] _blob;

        public Form1()
        {
            InitializeComponent();
        }

        private void btnZhuce_Click(object sender, EventArgs e)
        {
            string str = NetRecognizePic.CJY_UserReg(this.txtzUser.Text.Trim(), this.txtzPwd.Text.Trim());
            string stradd = "";
            if (GetTextByKey(str, "err_no") == "0")
            {
                stradd = "注册成功[账号:" + this.txtzUser.Text.Trim() + ",密码:" + this.txtzPwd.Text.Trim() + "],请您及时到官方网站(http://www.chaojiying.com)做必要的安全设置";
            }
            else
            {
                stradd = GetTextByKey(str, "err_str");
            }
            this.richTextBox1.Text += "[" + DateTime.Now.ToString("HH:mm:ss") + "]" + stradd + "\r\n";
        }

        private void txtPay_Click(object sender, EventArgs e)
        {
            string str = NetRecognizePic.CJY_UserPay(this.txtqUser.Text.Trim(), this.txtlpCard.Text.Trim());
            string stradd = "";
            if (GetTextByKey(str, "err_no") == "0")
            {
                stradd = "充值成功";
            }
            else
            {
                stradd = GetTextByKey(str, "err_str");
            }
            this.richTextBox1.Text += "[" + DateTime.Now.ToString("HH:mm:ss") + "]" + stradd + "\r\n";
        }

        private void button4_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process.Start("http://www.chaojiying.com/api-4.html");  
        }

        private void btnFile_Click(object sender, EventArgs e)
        {
            if (!(File.Exists(this.txtPicPath.Text.Trim())))
            {
                this.richTextBox1.Text += "[" + DateTime.Now.ToString("HH:mm:ss") + "]文件[" + this.txtPicPath.Text.Trim() + "]不存在" + "\r\n";
                return; 
            }

            string str = NetRecognizePic.CJY_RecognizeFile(this.txtPicPath.Text.Trim(), this.txtqUser.Text.Trim(), this.MD5String(this.txtqPwd.Text.Trim()), this.txtlpSoftId.Text.Trim(), this.txtlpCodeType.Text.Trim(),"0","0", "");
            string strerr = GetTextByKey(str, "err_str");
            if (strerr != "OK")
            {
                this.richTextBox1.Text += "[" + DateTime.Now.ToString("HH:mm:ss") + "]" + strerr + "\r\n";
                //MessageBox.Show(strerr);
                return;
            }

            string strpic_id = GetTextByKey(str, "pic_id");
            this.txtPicID.Text = strpic_id;

            string strpic_str = GetTextByKey(str, "pic_str");
            this.txtshibie.Text = strpic_str;


            this.richTextBox1.Text += "[" + DateTime.Now.ToString("HH:mm:ss") + "]识别结果:" + strpic_str + "\r\n";

        }

        private void btnPic_Click(object sender, EventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "图片文件(*.BMP;*.JPG;*.GIF)|*.BMP;*.JPG;*.GIF|All files (*.*)|*.*";
            openFileDialog.RestoreDirectory = true;
            openFileDialog.FilterIndex = 1;
            if (openFileDialog.ShowDialog() == DialogResult.OK)
            {
                txtPicPath.Text = openFileDialog.FileName;
                this.pictureBox1.ImageLocation = openFileDialog.FileName;

            }
        }

        private void btnBytes_Click(object sender, EventArgs e)
        {
            if (!(File.Exists(this.txtPicPath.Text.Trim())))
            {
                this.richTextBox1.Text += "[" + DateTime.Now.ToString("HH:mm:ss") + "]文件[" + this.txtPicPath.Text.Trim() + "]不存在" + "\r\n";
                return;
            }

            FileStream stream = null;
            try
            {
                stream = new FileStream(this.txtPicPath.Text.Trim(), FileMode.Open, FileAccess.Read);
                _blob = new byte[stream.Length];
                stream.Read(_blob, 0, (int)stream.Length);

            }
            catch (Exception ex)
            {
            }
            finally
            {
                stream.Close();
            }

            string str = NetRecognizePic.CJY_RecognizeBytes(_blob,_blob.Length,this.txtqUser.Text.Trim(), this.MD5String(this.txtqPwd.Text.Trim()), this.txtlpSoftId.Text.Trim(), this.txtlpCodeType.Text.Trim(),"0","0", "");
            string strerr = GetTextByKey(str, "err_str");
            if (strerr != "OK")
            {
                this.richTextBox1.Text += "[" + DateTime.Now.ToString("HH:mm:ss") + "]" + strerr + "\r\n";
                //MessageBox.Show(strerr);
                return;
            }

            string strpic_id = GetTextByKey(str, "pic_id");
            this.txtPicID.Text = strpic_id;

            string strpic_str = GetTextByKey(str, "pic_str");
            this.txtshibie.Text = strpic_str;


            this.richTextBox1.Text += "[" + DateTime.Now.ToString("HH:mm:ss") + "]识别结果:" + strpic_str + "\r\n";

        }

        private void button1_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process.Start("http://www.chaojiying.com/api-1.html");  
        }

        private void btnQuery_Click(object sender, EventArgs e)
        {
            string str = NetRecognizePic.CJY_GetScore(this.txtqUser.Text.Trim(), this.MD5String(this.txtqPwd.Text.Trim()));
                string stradd = "";
                if (GetTextByKey(str, "err_no") == "0")
                {
                    stradd = "题分" + GetTextByKey(str, "tifen");
                }
                else
                {
                    stradd = GetTextByKey(str, "err_str");
                }
                this.richTextBox1.Text += "[" + DateTime.Now.ToString("HH:mm:ss") + "]" + stradd + "\r\n";
        }

        /// <summary>
        /// 根据关键字获取JSON数据里面的信息
        /// </summary>
        /// <param name="jsonText"></param>
        /// <param name="key"></param>
        /// <returns></returns>
        public string GetTextByKey(string jsonText,string key)
        {
            JObject jsonObj = JObject.Parse(jsonText);
            string str = jsonObj[key].ToString();
            return str;
        }

        public string MD5String(string str)
        {
            if (str == "") return str;
            byte[] b = System.Text.Encoding.Default.GetBytes(str);
            return MD5String(b);
        }
        public static string MD5String(byte[] b)
        {
            b = new System.Security.Cryptography.MD5CryptoServiceProvider().ComputeHash(b);
            string ret = "";
            for (int i = 0; i < b.Length; i++)
                ret += b[i].ToString("x").PadLeft(2, '0');
            return ret;
        }

        private void button6_Click(object sender, EventArgs e)
        {
            string str = NetRecognizePic.CJY_ReportError(this.txtqUser.Text.Trim(), this.MD5String(this.txtqPwd.Text.Trim()), this.txtPicID.Text.Trim(), this.txtlpSoftId.Text.Trim());
            string stradd = "";
            if (GetTextByKey(str, "err_no") == "0")
            {
                stradd = "图片ID[" + this.txtPicID.Text.Trim() + "]报错成功";
                this.richTextBox1.Text += "[" + DateTime.Now.ToString("HH:mm:ss") + "]" + stradd + "\r\n";
            }
        }

        private void linkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            this.richTextBox1.Text = "";
        }
    }
}
