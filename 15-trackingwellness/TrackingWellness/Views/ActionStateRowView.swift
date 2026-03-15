//
//  ActionStateRowView.swift
//  TrackingWellness
//
//  Created by Zachary Sturman on 8/30/23.
//

import SwiftUI

struct ActionStateRowView: View {
    @ObservedObject var actionState: ActionState
    
    var body: some View {
        HStack {
            NavigationLink(destination: ActionStateDetailView(actionState: actionState)) {
                Text(actionState.title)
            }
        }
    }
}
