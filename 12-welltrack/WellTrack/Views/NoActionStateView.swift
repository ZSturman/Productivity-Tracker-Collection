//
//  NoActionStateView.swift
//  WellTrack
//
//  Created by Zachary Sturman on 8/15/23.
//

import SwiftUI

struct NoActionStateView: View {
    var body: some View {
        VStack {
            Text("No ActionStates yet")
                .font(.largeTitle.bold())
            Text("Maybe add one or something")
                .font(.callout)
        }
    }
}

struct NoActionStateView_Previews: PreviewProvider {
    static var previews: some View {
        NoActionStateView()
    }
}
