/*-----------------------------------------------------------------------------
A simple echo bot for the Microsoft Bot Framework.
-----------------------------------------------------------------------------*/

var restify = require('restify');
var builder = require('botbuilder');
var botbuilder_azure = require("botbuilder-azure");
var PythonShell = require('python-shell')

// Setup Restify Server
var server = restify.createServer();
server.listen(process.env.port || process.env.PORT || 5000, function () {
   console.log('%s listening to %s', server.name, server.url);
});

// Create chat connector for communicating with the Bot Framework Service
var connector = new builder.ChatConnector({
    appId: process.env.MicrosoftAppId,
    appPassword: process.env.MicrosoftAppPassword,
    openIdMetadata: process.env.BotOpenIdMetadata
});

// Listen for messages from users
server.post('/api/messages', connector.listen());

/*----------------------------------------------------------------------------------------
* Bot Storage: This is a great spot to register the private state storage for your bot.
* We provide adapters for Azure Table, CosmosDb, SQL Azure, or you can implement your own!
* For samples and documentation, see: https://github.com/Microsoft/BotBuilder-Azure
* ---------------------------------------------------------------------------------------- */

var tableName = 'botdata';
// var azureTableClient = new botbuilder_azure.AzureTableClient(tableName, process.env['AzureWebJobsStorage']);
// var tableStorage = new botbuilder_azure.AzureBotStorage({ gzipData: false }, azureTableClient);


var inMemoryStorage = new builder.MemoryBotStorage();


// Create your bot with a function to receive messages from the user
var bot = new builder.UniversalBot(connector);
bot.set('storage', inMemoryStorage);

bot.dialog('/', [
    // function (session) {
    //     builder.Prompts.text(session, "Hello... What's your name?");
    // },
    // function (session, results) {
    //     session.userData.name = results.response;
    //     builder.Prompts.number(session, "Hi " + results.response + ", How many years have you been coding?");
    // },
    // function (session, results) {
    //     session.userData.coding = results.response;
    //     builder.Prompts.choice(session, "What language do you code Node using?", ["JavaScript", "CoffeeScript", "TypeScript"]);
    // },
    // function (session, results) {
    //     session.userData.language = results.response.entity;
    //     session.send("Got it... " + session.userData.name +
    //                 " you've been programming for " + session.userData.coding +
    //                 " years and use " + session.userData.language + ".");
    // }
    // ,

    function (session) {
        session.send("Welcome to TripCone.");
        // builder.Prompts.time(session, "Please provide a reservation date and time (e.g.: June 6th at 5pm)");
        builder.Prompts.text(session, "Where are you travelling from?")
    },
    function (session, results) {
        // session.dialogData.reservationDate = builder.EntityRecognizer.resolveTime([results.response]);
        session.userData.fromCity = results.response;
        fromCity = results.response;

        builder.Prompts.text(session, "Where are you travelling to?");
    },
    function (session, results) {
        session.userData.toCity = results.response;
        toCity = results.response;

        // session.userData.partySize = results.response;
        builder.Prompts.number(session, "How many days are you travelling for?");
    },
    function (session, results) {
        session.userData.numDays = results.response;
        numDays = results.response;

        // Process request and display reservation details
        // session.send(`Reservation confirmed. Reservation details: <br/>Date/Time: ${session.userData.reservationDate} <br/>Party size: ${session.userData.partySize} <br/>Reservation name: ${session.userData.reservationName}`);
        session.send(`Information confirmed: <br/>From City: ${session.userData.fromCity} <br/>To City: ${session.userData.toCity} <br/>Number of days: ${session.userData.numDays}`);
        session.send('Gathering price information...');
        // session.endDialog();

        // const spawn = require('child_process').spawn;
        // const python = spawn('python', ['/Users/kenziyuliu/OneDrive/Hackathons/CapitalOne/cone/trip_estimator.py', '--from=' + fromCity, '--to=' + toCity, '--days=' + numDays])
        //
        // python.stdout.on('data', function(data) {
        //     console.log(data);
        //     console.log('DADADADADA');
        // });

        var fromArg = '--from=' + fromCity;
        var toArg = '--to=' + toCity;
        var daysArg = '--days=' + numDays;

        var options = {
          mode: 'text',
          pythonPath: '/usr/local/bin/python3',
          scriptPath: './',
          args: [fromArg, toArg, daysArg]
        };

            // console.log(fromArg);
            // console.log(toArg);
            // console.log(daysArg);

        PythonShell.run('trip_estimator.py', options, function (err, results) {
          if (err)
            throw err;
          // Results is an array consisting of messages collected during execution
          // console.log('results: %j', results);
          for (var i = 0; i < results.length; i++)
            session.send(results[i]);
        });

    }
]);








// var restify = require('restify');
// var builder = require('botbuilder');
//
// // Setup Restify Server
// var server = restify.createServer();
// server.listen(process.env.port || process.env.PORT || 5000, function () {
//    console.log('%s listening to %s', server.name, server.url);
// });
//
// // Create chat connector for communicating with the Bot Framework Service
// var connector = new builder.ChatConnector({
//     appId: process.env.MicrosoftAppId,
//     appPassword: process.env.MicrosoftAppPassword
// });
//
// // Listen for messages from users
// server.post('/api/messages', connector.listen());
//
// // // Receive messages from the user and respond by echoing each message back (prefixed with 'You said:')
// // var bot = new builder.UniversalBot(connector, function (session) {
// //     var msg = new builder.Message(session)
// //         .text("Thank you for expressing interest in our premium golf shirt! What color of shirt would you like?")
// //         .suggestedActions(
// //             builder.SuggestedActions.create(
// //                     session, [
// //                         builder.CardAction.imBack(session, "productId=1&color=green", "Green"),
// //                         builder.CardAction.imBack(session, "productId=1&color=blue", "Blue"),
// //                         builder.CardAction.imBack(session, "productId=1&color=red", "Red")
// //                     ]
// //                 ));
// //     session.send(msg);
// //
// //     // session.send("You said: %s", session.message.text);
// // });
//
// var inMemoryStorage = new builder.MemoryBotStorage();
//
// var fromCity = "";
// var toCity = "";
// var numDays = 0;
//
// var PythonShell = require('python-shell')
//
// // This is a dinner reservation bot that uses a waterfall technique to prompt users for input.
// var bot = new builder.UniversalBot(connector, [
//     function (session) {
//         session.send("Welcome to TripCone.");
//         // builder.Prompts.time(session, "Please provide a reservation date and time (e.g.: June 6th at 5pm)");
//         builder.Prompts.text(session, "Where are you travelling from?")
//     },
//     function (session, results) {
//         // session.dialogData.reservationDate = builder.EntityRecognizer.resolveTime([results.response]);
//         session.dialogData.fromCity = results.response;
//         fromCity = results.response;
//
//         builder.Prompts.text(session, "Where are you travelling to?");
//     },
//     function (session, results) {
//         session.dialogData.toCity = results.response;
//         toCity = results.response;
//
//         // session.dialogData.partySize = results.response;
//         builder.Prompts.number(session, "How many days are you travelling for?");
//     },
//     function (session, results) {
//         session.dialogData.numDays = results.response;
//         numDays = results.response;
//
//         // Process request and display reservation details
//         // session.send(`Reservation confirmed. Reservation details: <br/>Date/Time: ${session.dialogData.reservationDate} <br/>Party size: ${session.dialogData.partySize} <br/>Reservation name: ${session.dialogData.reservationName}`);
//         session.send(`Information confirmed: <br/>From City: ${session.dialogData.fromCity} <br/>To City: ${session.dialogData.toCity} <br/>Number of days: ${session.dialogData.numDays}`);
//         session.send('Gathering price information...');
//         // session.endDialog();
//
//         // const spawn = require('child_process').spawn;
//         // const python = spawn('python', ['/Users/kenziyuliu/OneDrive/Hackathons/CapitalOne/cone/trip_estimator.py', '--from=' + fromCity, '--to=' + toCity, '--days=' + numDays])
//         //
//         // python.stdout.on('data', function(data) {
//         //     console.log(data);
//         //     console.log('DADADADADA');
//         // });
//
//         var fromArg = '--from=' + fromCity;
//         var toArg = '--to=' + toCity;
//         var daysArg = '--days=' + numDays;
//
//         var options = {
//           mode: 'text',
//           pythonPath: '/usr/local/bin/python3',
//           scriptPath: './cone/',
//           args: [fromArg, toArg, daysArg]
//         };
//
//             // console.log(fromArg);
//             // console.log(toArg);
//             // console.log(daysArg);
//
//         PythonShell.run('trip_estimator.py', options, function (err, results) {
//           if (err)
//             throw err;
//           // Results is an array consisting of messages collected during execution
//           // console.log('results: %j', results);
//           for (var i = 0; i < results.length; i++)
//             session.send(results[i]);
//         });
//
//     }
// ]).set('storage', inMemoryStorage); // Register in-memory storage
//
//
