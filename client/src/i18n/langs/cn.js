import zhLocale from 'element-ui/lib/locale/lang/zh-CN'
const cn={
	Login:{
		'title':'登录',
		'username':'用户名/邮箱',
		'password':'密码',
		'RememberMe':'记住我',
		'Reg':'注册',
		'LogIn':'登录',
		'tip':'提示',
		'plsInp':'请输入帐号和密码',
		'wrongInp':'帐号或密码错误',
		'rules1':'用户名/邮箱不能为空',
		'rules2':'密码不能为空',
		'confirm':'确定',
	},
	Register:{
		'title':'注册',
		'email':'请输入您的邮箱地址',
		'username':'请输入您的用户名',
		'password':'请输入您的密码',
		'confirmpw':'请再次确认您的密码',
		'Uname':'请输入您的昵称',
		'back':'返回登录',
		'Reg':'注册',
		'hint':'提示',
		'WrongInp':'输入信息不正确',
		'Ok':'确定',
		'uReged':'用户名已被注册',
		'eReged':'邮箱已被注册',
		'retLogIn':'返回登录',
		'ret':'立即返回',
		'newerror':'两次输入的密码不一致',
		'e_message1':'请输入邮箱地址',
		'e_message2':'请输入正确的邮箱地址',
		'u_message1':'请输入用户名',
		'u_message2':'用户名的长度不得超过20个字符',
		'p_message1':'请输入密码',
		'p_message2':'密码长度为8～15位',
		'confirm_password':'请输入确认密码',
		'n_message':'昵称长度过长',
		'v_message':'验证码不正确',
		'Successful_Reg':'注册成功！',
		'BackLogIn':'秒后返回登录',
		'plsVerify':'请输入验证码',
		'verify':'获取验证码',
		
	},
	main:{
		'welcome':'欢迎，',
		'logout':'注销',
		'home':'用户主页',
		'history':'历史记录',
		'new':'新建评分'
	},
	usermain:{
		'noRecord':'您还没有评分记录。',
		'title':'题目：',
		'score':'得分：',
		'more':'更多',
		'usage':'当前使用',
		'times':'次',
		'max':'当前最高',
		'score':'分',
	},
	historyPage:{
		'range':'统计时间范围：',
		'to':'至',
		'StartDate':'开始日期',
		'endDate':'截止日期',
		'typos':'错别字',
		'wrongtimes':'错误次数',
		'pickerOptions1':'最近一周',
		'pickerOptions2':'最近一个月',
		'pickerOptions3':'最近三个月',
		'times':'次数',
		'level':'等级',
		'score':'分值',
	},
	New:{
		'scoring':'正在计算得分',
		'Title':'题目：',
		'plsArticle':'请输入正文：',
		'length':'字数：',
		'commit':'提交',
		'tips':'题目或文章格式不正确',
		'confirm':'确定',
		'tip':'提示',
		'title_tip1':'题目不能为空',
		'title_tip2':'题目长度过长',
		'article_tip1':'文章不能为空',
		'article_tip2':'文章长度过长'
	},
	Result:{
	  'Title':'题目：',
	  'Score':'总得分：',
	  'VocabularyD':'词汇分布',
	  'Item':'分项得分',
	  'Voca':'词汇水平',
	  'Relevance':'切题程度',
	  'Sentence':'句型难度',
	  'Expression':'表述准确',
	  'ArticleLen':'篇幅长度',
	  'FullText':'全文点评',
	  'Comment':'原文点评',
	  'Development':'词汇拓展',
	  'HSK1':'HSK一级',
	  'HSK2':'HSK二级',
	  'HSK3':'HSK三级',
	  'HSK4':'HSK四级',
	  'HSK5':'HSK五级',
	  'HSK6':'HSK六级'
	},
	...zhLocale
}

export default cn;