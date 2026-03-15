//
//  NoActionStatesView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/2/23.
//

import SwiftUI

struct NoActionStatesView: View {
    var body: some View {
        VStack {
            Text("No ActionStates yet")
                .font(.title2)
                .bold()
            Text("Go ahead. Add one")
                .font(.caption)
        }
    }
}

struct NoActionStatesView_Previews: PreviewProvider {
    static var previews: some View {
        NoActionStatesView()
    }
}
