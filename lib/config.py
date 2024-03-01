# Configure markers
shell_path = "assets/shells/"
filename_marker = "*filename*"
data_marker = "*data*"
mimetype_marker = "*mimetype*"

# Configure HTTP Protocol
protocol = 'https'

# Configure modules name
active_modules = [
    "extension_shuffle",
    "double_extension",
    "discrepancy",
    "forward_double_extension",
    "reverse_double_extension",
    "stripping_extension",
    "null_byte_cutoff",
    "name_overflow_cutoff",
    "htaccess_overwrite",
    "svg_xxe",
    "svg_xss"
]

# Modules that you do not want to scan with Anti-Malware and Detection mode
dont_scan_module = ['svg_xss', 'svg_xxe', 'htaccess_overwrite']

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
