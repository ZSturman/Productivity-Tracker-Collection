//
//  ActionStateExecutionApp.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/27/23.
//

import SwiftUI

@main
struct ActionStatesApp: App {
    @StateObject private var dataController = DataController()
    

//    init() {
//        let dataController = DataController()
//        _dataController = StateObject(wrappedValue: dataController)
//    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, dataController.container.viewContext)
        }
    }
}
