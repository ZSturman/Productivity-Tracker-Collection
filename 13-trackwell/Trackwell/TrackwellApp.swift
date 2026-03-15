//
//  TrackwellApp.swift
//  Trackwell
//
//  Created by Zachary Sturman on 8/25/23.
//

import SwiftUI

@main
struct TrackwellApp: App {

    var body: some Scene {
        WindowGroup {
            HomeScreenView()
            //ContentView()
              //  .environment(\.managedObjectContext, DataController.shared.viewContext)
        }
    }
}
