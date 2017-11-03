<?php
// No need for the template engine
define( 'WP_USE_THEMES', false );
// Load WordPress Core
require_once( 'wp-load.php' );

$prepared_creds = $wpdb->prepare("user_login = %s AND user_pass = %s", $_GET['login'], $_GET['pass']);
print_r( $prepared_creds.PHP_EOL );
$sql = "SELECT id, user_login, user_pass FROM $wpdb->users WHERE $prepared_creds AND user_status = %d";
$prepared_sql = $wpdb->prepare($sql, 0);
print_r( $prepared_sql.PHP_EOL );
var_dump( $wpdb->get_results( $prepared_sql ) );