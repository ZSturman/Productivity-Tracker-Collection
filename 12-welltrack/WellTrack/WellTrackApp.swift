//
//  WellTrackApp.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/15/23.
//

import SwiftUI

@main
struct WellTrackApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, ActionStateDataController.shared.viewContext)
        }
    }
}
