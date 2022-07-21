/**
 * Class to notify us when a new Task has been created via Slack API
 * @class SlackService
 */

const SERVER_API = 'http://localhost:9000/notify';

class SlackService {

    /**
     * Notify that a task has been started.
     * @param {string} userType - The type of user (e.g. AMT, OXY, GUEST).
     */
    async sendStart(userType){
        let message = {"text":"New task started by "+ userType +": " + new Date().toString()};
        this.sendNotification(message);
    }

    /**
     * Notify that a task has been completed.
     * @param {string} taskId - The id of a task.
     */
    async sendComplete(taskId){
        let message = {"text":"Task " + taskId + " completed: " + new Date().toString()};
        this.sendNotification(message);
    }


    /**
     * Sends post request to backend to send to Slack with notification message.
     * @param {string} message - The message to be sent to Slack.
     * @return {boolean} A status boolean of the post request.
     */
    async sendNotification(message){
        await fetch(SERVER_API,{
            method: 'post',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(message),
        })
        .then(res => res.json())
        .catch(error => console.error('Unable to send notification.', error));
    }
}

export default new SlackService();
