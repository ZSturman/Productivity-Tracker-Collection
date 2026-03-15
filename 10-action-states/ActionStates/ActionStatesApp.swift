//
//  ActionStatesApp.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/22/23.
//
import SwiftUI

@main
struct ActionStatesApp: App {
    @StateObject private var dataController = DataController()
    @StateObject var listViewModel: ListsViewModel
    @StateObject var listItemViewModel: ListItemViewModel
    

    init() {
        let dataController = DataController()
        _dataController = StateObject(wrappedValue: dataController)
        let listViewModel = ListsViewModel(container: dataController.container)
        _listViewModel = StateObject(wrappedValue: listViewModel)
        let listItemViewModel = ListItemViewModel(container: dataController.container)
        _listItemViewModel = StateObject(wrappedValue: listItemViewModel)
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView(listItemViewModel: listItemViewModel)
                .environmentObject(listViewModel)
        }
    }
}
