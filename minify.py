'''
Created on Aug 23, 2013

@author: yali
'''

import fnmatch
import os
import subprocess
import sys

MINIFIED_SUB_EXT = ['.min', '-min']
NO_MINIFY_FILES = ['*/protected/tests/vendor/*', '*/yii/*']
NO_UPDATE_FILES = [ \
    'bootstrap.min.js', \
    'bootstrap.min.css', \
    'bootstrap-theme.min.css', \
    'bootstrap-3.1.1.min.js', \
    'bootstrap-3.1.1.min.css', \
    'bootstrap-theme-3.1.1.css', \
    'jquery-1.10.2.min.js', \
    'jquery-ui-1.10.3.min.js', \
    'jquery-ui-1.10.3.min.css', \
    'jquery-ui-i18n-1.10.3.min.js' \
]
SVN_USERNAME = 'unbuilder'
SVN_PASSWORD = 'Summer_14'
SVN_OPTIONS = '--non-interactive --trust-server-cert --no-auth-cache --username %s --password %s'

def shellExec(cmd, successMsg=None, errorMsgPrefix='Shell cmd execution failed: '):
    '''
    Executes a shell command and returns whether there was any error.
    
    @param cmd: the shell command.
    @param successMsg: the message to print to standard output if there was no error.
    @param errorMsgPrefix: the prefix of error message to print to standard output if there was any error.
    
    @return: returns whether there was any error.
    '''

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        if successMsg:
            print successMsg

        if output:
            print output

        return True
    except subprocess.CalledProcessError as cpe:
        msgFormat = '\n    '.join([
            errorMsgPrefix, \
            'Command: %s', \
            'Return code: %d', \
            'Output: %s' \
        ])
        print msgFormat % (cpe.cmd, cpe.returncode, cpe.output)
        return False
    except:
        # etype, evalue, etraceback = sys.exc_info()
        print 'Unexpected error:', sys.exc_info()[0]
        return False

def isMinified(filename):
    filename = os.path.split(filename)[1]
    namepart = os.path.splitext(filename)[0]
    subext = namepart[-4:]
    return subext.lower() in MINIFIED_SUB_EXT

def nominify(filename):
    nodir = os.path.split(filename)[1]
    namepart = os.path.normcase(nodir)
    for pattern in NO_MINIFY_FILES:
        if namepart == os.path.normcase(pattern) or fnmatch.fnmatch(namepart, pattern) or fnmatch.fnmatch(filename, pattern):
            return True

    return False

def noupdate(filename):
    nodir = os.path.split(filename)[1]
    namepart = os.path.normcase(nodir)
    for pattern in NO_UPDATE_FILES:
        if namepart == os.path.normcase(pattern) or fnmatch.fnmatch(namepart, pattern) or fnmatch.fnmatch(filename, pattern):
            return True

    return False

def olderThan(leftFile, rightFile):
    return os.path.getmtime(leftFile) < os.path.getmtime(rightFile)

def findMinifiedVersion(unminifiedFileName):
    filename, ext = os.path.splitext(unminifiedFileName)
    for subext in MINIFIED_SUB_EXT:
        minified = filename + subext + ext
        if os.path.isfile(minified):
                return minified

def minify(srcDir, forceMinify=False):
    cwd = os.path.dirname(os.path.realpath(__file__))

    jsjar = os.path.normpath(os.path.join(cwd, 'closurecompiler/compiler.jar'))
    jsmin = 'java -jar "' + jsjar + '" --js "%s" --js_output_file "%s"'

    cssjar = os.path.normpath(os.path.join(cwd, 'yuicompressor/yuicompressor-2.4.7.jar'))
    cssmin = 'java -jar "' + cssjar + '" "%s" --type css --charset utf-8 -o "%s"'

    mincmd = { '.js': jsmin, '.css': cssmin }

    for root, dirs, files in os.walk(srcDir):
        for thefile in files:
            name, ext = os.path.splitext(thefile)
            mincmdformat = mincmd.get(ext.lower())
            if not mincmdformat or isMinified(thefile):
                continue

            srcfile = os.path.join(root, thefile)
            if nominify(srcfile):
                print 'Skipped from minifying: ' + srcfile
                continue

            minfile = findMinifiedVersion(srcfile)
            if minfile:
                if noupdate(minfile):
                    print 'Skipped from updating: ' + minfile
                    continue

                if olderThan(srcfile, minfile) and not forceMinify:
                    print 'Previously minified: ' + minfile
                    continue
            else:
                minfile = os.path.join(root, name + MINIFIED_SUB_EXT[0] + ext)

            cmd = mincmdformat % (srcfile, minfile)
            print cmd
            if not shellExec(cmd):
                return False

    return True

def svn_checkout(workCopyPath, sourceUrl, quiet=False):
    svnOptions = '--quiet --ignore-externals ' + SVN_OPTIONS if quiet else SVN_OPTIONS
    cmd = 'svn checkout %s "%s" "%s"' % (svnOptions, sourceUrl, workCopyPath)
    print 'Checking out "%s" into "%s"...' % (sourceUrl, workCopyPath)
    return shellExec(cmd)

def svn_update(workCopyPath, quiet=False):
    svnOptions = '--quiet --ignore-externals ' + SVN_OPTIONS if quiet else SVN_OPTIONS
    cmd = 'svn update %s "%s"' % (svnOptions, workCopyPath)
    print 'Updating "%s"...' % workCopyPath
    return shellExec(cmd)

def svn_status(workCopyPath, quiet=False):
    svnOptions = '--quiet --ignore-externals ' + SVN_OPTIONS if quiet else SVN_OPTIONS
    cmd = 'svn status %s "%s"' % (svnOptions, workCopyPath)
    print 'Workcopy changes: (it will be blank if there are no changes)'
    return shellExec(cmd)

def svn_add(workCopyPath, quiet=False):
    cmd = 'svn add --quiet' if quiet else 'svn add'
    cmd += ' --force %s/* --auto-props --parents --depth infinity' % workCopyPath
    return shellExec(cmd)

def svn_checkin(workCopyPath, message='[MinifyJsCss]: checked in by running minify.py', quiet=False):
    svnOptions = '--quiet ' + SVN_OPTIONS if quiet else SVN_OPTIONS
    cmd = 'svn commit %s --message "%s" "%s"' % (svnOptions, message, workCopyPath)
    print 'Checking in...(it will be blank if there are no changes)'
    return shellExec(cmd)

def parseArgs():
    global NO_MINIFY_FILES
    global NO_UPDATE_FILES
    global SVN_USERNAME
    global SVN_PASSWORD
    global SVN_OPTIONS

    args = {}
    for arg in sys.argv[1:]:
        lowerArg = arg.lower()
        if lowerArg[:7] == '--force':
            args['force'] = True
        elif lowerArg[:6] == '--svn=':
            args['svn'] = arg[6:]
        elif lowerArg[:14] == '--svnusername=':
            SVN_USERNAME = arg[14:]
        elif lowerArg[:14] == '--svnpassword=':
            SVN_PASSWORD = arg[14:]
        elif lowerArg[:10] == '--nominify':
            NO_MINIFY_FILES.append(arg[11:])
        elif lowerArg[:10] == '--noupdate':
            NO_UPDATE_FILES.append(arg[11:])
        else:
            args['dir'] = arg

    SVN_OPTIONS = SVN_OPTIONS % (SVN_USERNAME, SVN_PASSWORD)
    return args

def printUsage():
    print '''python minify.py [--svn=URL] [--force] [--nominify=FILENAME] [--noupdate=FILENAME] PATH

    --svn=URL                    Optional, source files will be checked out from the URL, minified, then checked in.
                                 If this option is specified, PATH should be an empty directory.

    --svnusername=USERNAME       Subversion username, defaults to 'svc-ldap-usher'.

    --svnpassword=PASSWORD       Subversion password, defaults to 'BiSA4whA'.

    --force                      Optional, re-generate all existing minified files.
                                 If this option isn't specified, existing minified files will be updated only if
                                 Corresponding unminified file is newer.

    --nominify=FILENAME          Optional, skip FILENAME from minifying; you can use wildcards in FILENAME.
                                 To skip multiple files, use this option multiple times.
                                 Note: this option still takes effect if "--force" was specified.

    --noupdate=FILENAME          Optional, if FILENAME is a minified file, don't update it; you can use wildcards.
                                 To preserve multiple minified files, use this option multiple times.
                                 Note: this option still takes effect if "--force" was specified.

    PATH                         Required, the path to the root directory of source files; 
                                 If --svn option is specified, 
                                 It means the path to the directory where source files will be saved in.
'''

def isDirEmpty(directory):
    return not os.listdir(directory)

def main():
    args = parseArgs()
    if not args:
        printUsage()
        return 0

    workingDir = args.get('dir')
    if not workingDir:
        print 'Please specify the directory of sources to minify.'
        return 1

    workingDir = os.path.normpath(workingDir)

    subversion = args.get('svn')
    if subversion:
        if os.path.isdir(workingDir) and not isDirEmpty(workingDir):
            if not svn_update(workingDir, True):
                print 'Failed to update subversion work copy: ' + workingDir
                return 2
        elif not svn_checkout(workingDir, subversion, True):
            return 5

    if not os.path.isdir(workingDir):
        print 'Directory not found: ' + workingDir
        return 3

    if not minify(workingDir, args.get('force')):
        return 4

    if subversion:
        if not (svn_add(workingDir) and svn_status(workingDir) and svn_checkin(workingDir)):
            return 5

    return 0

if __name__ == '__main__':
    exitCode = main()
    if exitCode != 0:
        sys.exit(exitCode)
