const { execSync } = require('child_process');
const core = require('@actions/core');
const { exec } = require('@actions/exec');

async function run() {
  try {
    // Get environment variables
    const username = core.getInput('SSH_USERNAME');
    const ipAddress = core.getInput('SSH_IPADDRESS');
    const password = core.getInput('SSH_PASSWORD');
    const localPath = core.getInput('LOCAL_PATH');
    const remotePath = core.getInput('REMOTE_PATH');

    // Install sshpass
    console.log('Installing sshpass...');
    await exec('sudo apt-get update && sudo apt-get install -y sshpass');

    // Construct the rsync command
    const rsyncCommand = [
      `sshpass -p "${password}" rsync -rv`,
      `-e "ssh -o StrictHostKeyChecking=no"`,
      `"${localPath}"`,
      `"${username}@${ipAddress}:${remotePath}"`,
      `--exclude .git`
    ].join(' ');

    // Run the rsync command
    console.log('Running rsync...');
    execSync(rsyncCommand, { stdio: 'inherit' });

    console.log('Deployment completed successfully.');
  } catch (error) {
    core.setFailed(`Deployment failed: ${error.message}`);
  }
}

run();
